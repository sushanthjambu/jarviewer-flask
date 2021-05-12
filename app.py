"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, render_template
from botocore.exceptions import ClientError
import boto3, os, logging, json, botocore
app = Flask(__name__)

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

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #app.run(HOST, PORT)
    app.run(host = "0.0.0.0", port = PORT)
