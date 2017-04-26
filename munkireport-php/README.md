## Overview
Elastic beanstalk is arguably the easiest way to get a Munkireport server up and running. This demo is making use of the EB CLI. You can also upload a zip file including your Munkireport `config.php` using the GUI. But this is more fun!


### Requirements
* AWS Account
* AWS profile setup with administrative permissions
  * See [here](http://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html) for how to setup a user with administrative permissions
  * And [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) to setup a profile
* EB CLI
  * Installed in virtualenv via pip is preferred

### Steps

##### Clone the latest version of Munkireport
```
git clone https://github.com/munkireport/munkireport-php.git
```

##### Setup free tier RDS instance - (optional)
*_You can use the default sqlite database and totally skip this section. For production setup please use a dedicated database server_*  
You are welcome to use the GUI for this too but this command will do most of it for you. Make sure  `YOURDBUSERNAME` and `YOURDBPASSWORD` are complex!!
```
aws rds create-db-instance \
    --db-instance-identifier munkireport \
    --db-instance-class db.t2.micro \
    --engine mysql \
    --allocated-storage 5 \
    --db-name munkireport \
    --master-username <YOURDBUSERNAME> \
    --master-user-password <YOURDBPASSWORD>
```

##### Setup virtualenv and install EB CLI
You are welcome to install the EB CLI any way you want. I personally recommend using a virtualenv as it is IMHO the simplest way to explain.

Install virtualenv and pip
```
sudo easy_install virtualenv
sudo easy_install pip
```
From here on out we'll be working from inside the munkireport-php folder.
```
cd munkireport-php
```

Now create a virtualenv and install the EB CLI
```
virtualenv .env
source .env/bin/activate
pip install awsebcli
```
You should now be able to type `eb` in the prompt and have the help displayed

##### Setup elastic beanstalk application

```
eb init
```
Then follow the prompts. The region and ssh parts are up to you. You need to answer `y` to PHP and `4` to select PHP 7.0. You can forget about CodeCommit so answer `n` there.
```
Select a default region
1) us-east-1 : US East (N. Virginia)
2) us-west-1 : US West (N. California)
3) us-west-2 : US West (Oregon)
4) eu-west-1 : EU (Ireland)
5) eu-central-1 : EU (Frankfurt)
6) ap-south-1 : Asia Pacific (Mumbai)
7) ap-southeast-1 : Asia Pacific (Singapore)
8) ap-southeast-2 : Asia Pacific (Sydney)
9) ap-northeast-1 : Asia Pacific (Tokyo)
10) ap-northeast-2 : Asia Pacific (Seoul)
11) sa-east-1 : South America (Sao Paulo)
12) cn-north-1 : China (Beijing)
13) us-east-2 : US East (Ohio)
14) ca-central-1 : Canada (Central)
15) eu-west-2 : EU (London)
(default is 3):

Enter Application Name
(default is "mr-test"):
Application mr-test has been created.

It appears you are using PHP. Is this correct?
(Y/n): y

Select a platform version.
1) PHP 5.4
2) PHP 5.5
3) PHP 5.6
4) PHP 7.0
5) PHP 5.3
(default is 1): 4
Note: Elastic Beanstalk now supports AWS CodeCommit; a fully-managed source control service. To learn more, see Docs: https://aws.amazon.com/codecommit/
Do you wish to continue with CodeCommit? (y/N) (default is n): n
Do you want to set up SSH for your instances?
(Y/n): n
```

##### Edit `.gitignore`
The `eb create` and `eb deploy` actions use git for versioning. Munkireport is ignoring files that we need to be tracking so you'll need to delete the following lines from `.gitignore`
* `config.php`
* `app/db/*`

##### Edit config
 Munkireport needs a config with an admin user and database configured. The default database settings will use sqlite, sqlite is probably not the best for production but is ok for testing. Keep in mind that for autoscaling to work you'll need to use the RDS instance or some other dedicated database server.

##### Commit your changes
Now we need to commit your changes to the `.gitignore` file and `config.php`
```
git add config.php .gitignore
git commit -m "my munkireport config"
```

##### Deploy environment
The moment we been waiting for. `eb create` will ask us some more questions but then we should be able to start using our application.
```
bash$ eb create
Enter Environment Name
(default is mr-test-dev):
Enter DNS CNAME prefix
(default is mr-test-dev):

Select a load balancer type
1) classic
2) application
(default is 1): 1
```

You can open the app by running
```
eb open
```
Or check the status
```
eb status
```
##### Updating your application
Because git is being used by Elastic Beanstalk you'll need to commit (not push) changes before updating your application.
```
git commit -am "New config"
eb update
```

### That's IT!!
If you made it this far Munkireport should be up and running. Hit me up on [macadmins slack](https://macadmins.org/) `@wrobson` if you get stuck.
