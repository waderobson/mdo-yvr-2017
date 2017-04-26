## Overview
Take advantage of the limitless scaling and the low cost of serverless architecture by using Zappa to host Sal in AWS Lambda.

Thanks to Zappa there's just a few lines we need to add to `settings.py` to get Sal deployed to AWS Lambda.

AWS Lambda is a [FaaS](https://en.wikipedia.org/wiki/Function_as_a_Service) and the functions, by themselves, need to be triggered. Zappa makes use of Api Gateway to trigger Lambda, handing the web requests and responses between your app and the client.

### Requirements
* AWS Account
* AWS profile setup with administrative permissions
  * See [here](http://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html) for how to setup a user with administrative permissions
  * And [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) to setup a profile
* [Homebrew](https://brew.sh/)
* 2 S3 buckets
  * one public, for the static assets and
  * one private, to upload the code to. (Zappa will handle creating this one)
* IAM user that can write to the static assets bucket

### Steps

##### Clone the latest version of Sal
```
git clone https://github.com/salopensource/sal.git
```

##### Clone this repo
```
git clone https://github.com/waderobson/mdo-yvr-2017.git
```

##### Setup free tier RDS instance
You are welcome to use the GUI for this too but this command will do most of it for you. The unfortunate thing with this is that it won't really work without being publicly available so make sure  `YOURDBUSERNAME` and `YOURDBPASSWORD` are complex!!
```
aws rds create-db-instance \
    --db-instance-identifier sal \
    --db-instance-class db.t2.micro \
    --engine postgres \
    --allocated-storage 5 \
    --db-name sal \
    --master-username <YOURDBUSERNAME> \
    --master-user-password <YOURDBPASSWORD>
```
It will take a few minutes to come online

##### Copy configuration
You'll need a couple files from this repo to your Sal repo.
```
cd sal
cp ../mdo-yvr-2017/sal/requirements-zappa.txt .
cp ../mdo-yvr-2017/sal/zappa-settings.py ./sal/settings.py
```

##### Edit configuration
Open `settings.py` in a text editor of your choice and fill out the S3 and database sections.

##### Install postgresql
You need to install postgresql for psycopg2 to build.
```
brew install postgresql
```

##### Create a virtual environment
Zappa bundles the packages that support Sal, for example django, based off the packages installed in your active virtual environment. It is not only recommended, but required for Zappa to work.
```
virtualenv .env
source .env/bin/activate
pip install six
pip install -r requirements-zappa.txt
```

##### Upload assets to S3

```
python manage.py collectstatic
```
##### Configure CORS on assets bucket
```
aws s3api put-bucket-cors --bucket MyBucket --cors-configuration file://cors.json
```

##### Migrate Db
```
python manage.py migrate
```

##### Create sal admin user
```
python manage.py createsuperuser
```
##### Clean up .pyc
This needs to be run before deploying or updating if you've used `manage.py` to preform operations locally.
```
find server -name \*.pyc -exec rm {} \;
```
##### Zappa
First thing you'll need to do is run `zappa init` this will create `zappa_settings.json` and add some sane defaults. Using the defaults is best except for the settings, you'll be presented with lots of options make sure you chose `sal.settings`.
```
zappa init
```
Now you can deploy your code.
```
zappa deploy
```
For any updates after that run
```
zappa update
```

### That's IT!!
If you made it this far Sal should be up and running. Hit me up on [macadmins slack](https://macadmins.org/) `@wrobson` if you get stuck.
