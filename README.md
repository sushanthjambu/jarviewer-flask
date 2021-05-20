# A Flask Server connected to Amazon S3 - Deployed on Heroku
This is a simple server side implementation that is used for the WebAR feature in another repo mentioned below.
> https://github.com/sushanthjambu/unityarapp

# How To
1. You will need to create or use an existing Amazon S3 bucket.
    - If you already have an AWS account and are using S3 service you may use them.
    - If you don't have an AWS account you may create a new account so that you will get 12 month free-tier account. Using this you can create an S3 bucket and configure it here.
      > **Note : There are monthly usage limits even for free-tier S3 service please go through them as you may be billed if you exceed these limits.**
2. You can directly create a new app on Heroku and clone it from this repo. Alternately you may download this repo and push to Heroku using Heroku CLI.
    - For Heroku app to deploy properly, you have to set a few config variables.
      1. `heroku config:set AWS_ACCESS_KEY_ID=your_aws_access_key -a your_app_name`
      2. `heroku config:set AWS_SECRET_ACCESS_KEY=your_secret_aws_access_key -a your_app_name`
      3. `heroku config:set S3_BUCKET=your_amazon_s3_bucket_name -a your_app_name`
    - You must also provision a database to your app. This project uses heroku-postgres. To provision database from CLI use command
      ```heroku addons:create heroku-postgresql:hobby-dev -a your_app_name```
      This provisions a free heroku-postgres addon to your app. For more info visit https://devcenter.heroku.com/articles/heroku-postgresql
    - Provisioning a database automatically creates a config variable `DATABASE_URL`. Make sure the `DATABASE_URL` config var is set using the command `heroku config -a your_app_name` which lists all your app's config vars.
    > Note : You must also change the region name of S3 bucket [here](https://github.com/sushanthjambu/jarviewer-flask/blob/ab15102d0cd513c5c9747c02d9b659a8c96dd06d/app.py#L31)
    
For more info on deploying a flask app to heroku check the link below.
- https://devcenter.heroku.com/articles/s3-upload-python
