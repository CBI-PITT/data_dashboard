# data_dashboard

## Installation
#### Backend:
`conda install elasticsearch`

`pip install flask flask_cors flask_login flask_sqlalchemy flask_admin pandas numpy elasticsearch_dsl pymysql mysqlclient`

install MySQL dependencies:

`sudo apt-get install build-essential libapache2-mod-wsgi-py3 libmysqlclient-dev`

`sudo apt install mysql-server`

create database and user:

`mysql> CREATE DATABASE dashboard`

`mysql> CREATE USER 'dev'@'localhost' IDENTIFIED BY 'password';`

`mysql> grant all privileges on *.* to 'dev'@'localhost';`

`mysql> INSERT INTO admin_credentials (id, account , password) VALUES (1, 'dev', 'password');`

`cd flask-server`

`python server.py`

#### Elasticsearch:
`docker network create elastic`

`docker run --name elasticsearch --net elastic -p 9200:9200 -v /CBI_FastStore/Iana/BIL/data_mining_dashboard/elasticsearch/data:/usr/share/elasticsearch/data -e discovery.type=single-node -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:8.2.2`

`docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.2.2`

`cd es_importing`

`python importing.py`

#### Frontend:
`nvm install v16.20.1`

`cd dashboard`

`npm install`

`npm start`

## To start provisioned dashboard:

`docker start <elasticsearch_container_id>`

`docker start <kibana_container_id>`

`cd data_dashboard`

`python flask-server/server.py`

`cd ../dashboard`

`npm start`
