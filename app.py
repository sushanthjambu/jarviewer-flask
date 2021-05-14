"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, render_template, g, Response, url_for
from botocore.exceptions import ClientError
import boto3, os, logging, json, botocore
import psycopg2
from psycopg2 import pool
from hashids import Hashids

app = Flask(__name__)

hashids = Hashids(min_length=5, salt=os.environ.get('AWS_SECRET_ACCESS_KEY'))


# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app

@app.route('/')
def hello():
    """Renders a sample page."""
    return "Jambu AR : Server"

@app.route('/sign_request/', methods = ['GET'])
def presigned_request():
    S3_BUCKET = 'jambuartest'
    filename = request.args.get('file_name')

    s3 = boto3.client('s3', config = botocore.client.Config(region_name = 'ap-south-1', signature_version = 's3v4'))
    try:
        presigned_post = s3.generate_presigned_post(S3_BUCKET, filename,
                                                    Fields = {"acl": "public-read"},
                                                    Conditions = [{"acl": "public-read"}],
                                                    ExpiresIn = 60)
    except ClientError as e:
        logging.error(e)
        return None
    return json.dumps(presigned_post)

def get_db():
    if 'db' not in g:
        DATABASE_URL = os.environ['DATABASE_URL']
        g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
        #g.db = psycopg2.connect(database='jarviewer', user='postgres', password='ceasar1@3')

    return g.db

@app.teardown_appcontext
def close_conn(e):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/save_url', methods = ['POST'])
def save_to_database():
    db = get_db()
    object_url = request.form['Location']
    if object_url is None:
        return Response("URL not received", status = 400)
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO objecturl (url) VALUES (%s) RETURNING id;", (object_url,))
        db.commit()
        row_id = cur.fetchone()[0]
        hash_id = hashids.encode(row_id)
        cur.close()
        return request.url_root + url_for('display_ar', hash=hash_id)[1:]
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        cur.close()
        db.rollback()
        return Response("URL could not be saved to Database", status = 400)

@app.route('/j_arviewer/<hash>', methods = ['GET'])
def display_ar(hash):
    row = hashids.decode(hash)
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("SELECT url FROM objecturl WHERE id = %s;", (row,))
        url_source = cur.fetchone()[0]
        cur.close()
        return render_template("index.html", aws_url=url_source)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        cur.close()
        return Response("Object not found in Database", status = 404)

    



if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #app.run(HOST, PORT)
    app.run(host = "0.0.0.0", port = PORT)
