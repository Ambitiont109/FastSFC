FastSFC
======================

## Dependencies

FastSFC's webapp runs on Django, React and MySQL. You will need the following dependencies in order to set it up:

* pip 19.0.3
* Python 2.7.10
* Node 10.15.1
* NPM 6.9.0
* npm-run-all 4.1.5

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
python manage.py migrate
```

**Install frontend dependencies**
```
npm install
```

**Start project**
```
run-p watch start
```

## Deployment
```
cd ansible
ansible-playbook -i production webservers.yml
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