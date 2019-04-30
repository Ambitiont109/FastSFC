FastSFC
======================

## Dependencies

FastSFC's webapp runs on Django, React and MySQL. You will need the following dependencies in order to set it up:

* pip 19.0.3
* python 2.7.10
* node 10.15.1
* npm 6.9.0
* npm-run-all 4.1.5

## Deployment structure

FastSFC is deployed with the following servers:

1. DB server: MySQL hosted on Amazon RDS
2. Search DB server: ElasticSearch hosted on ElasticCloud
3. Web server: React client and Django server (i.e. code in this repo) hosted on EC2
4. Compute server: Scraper code (i.e. code in scraper repo) hosted on EC2 that runs periodic cron jobs to fetch companies and documents

## Setup

**Create virtualenv for project**
```
pip install virtualenv
virtualenv env
source env/bin/activate
```

**Clone repository, install packages and configure settings**
```
cd path/to/app/repository
pip install -r requirements.pip
cp app/settings/local.sample.py app/settings/local.py
```

**Create and prepare MySQL database**
Ensure DATABASES in app/settings/local.py is configured to connect to MySQL database
```
mysql -u {{ mysql_user }}
create database {{ db_name }}
exit
```

** Seed database**

Download and install seed database from [url](https://drive.google.com/file/d/1WbX110mSqSZDD9u_4XRVgceOQQfAuiQI/view?usp=drive_open).

Migrate to update table structure.
```
python manage.py migrate
```

**Install frontend dependencies**
```
npm install
```

**Start project**
```
npm run-script start
```

## Deployment
```
npm run-script deploy:web
npm run-script deploy:compute
```

## Scraper (Optional)

FastSFC is comprised of a webapp (django) and scraper (scrapy). If you have access to the scraper module and would like to use it with the webapp, you may clone it as follows:

```
git clone https://justinyek@bitbucket.org/justinyek/fast-crawler.git scraper
```

## Documentation [NOT UPDATED]

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.