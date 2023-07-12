# data_dashboard

## Installation
#### Backend:
`conda install elasticsearch`

`pip install flask flask_cors pandas numpy`

`cd flask-server`

`python server.py`

#### Elasticsearch:
`docker run --name elasticsearch --net elastic -p 9200:9200 -e discovery.type=single-node -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:8.2.2`

`docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.2.2`

`cd es_importing`

`python importing.py`

#### Frontend:
`nvm install v16.20.1`

`cd dashboard`

`npm install`

`npm start`
