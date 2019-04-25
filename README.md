FastSFC
======================

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
pip install -e .
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
run-p watch server
```

## Deployment
```
cd ansible
ansible-playbook -i production webservers.yml
```

## Documentation

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.