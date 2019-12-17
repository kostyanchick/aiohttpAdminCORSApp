## Simple shop api
(tested with python 3.7)
***
### Setup 

#### Python requirements

To start you need to have installed python 3.7

Firstly create virtual environments for project
And activate it

```
python3.7 -m venv venv
source /venv/bin/activate
```

install packages from requirements.txt located at root path:

``pip install requirements.txt``
***
#### Mongo setup
To run postgres in docker just run the command. Will be bound to port 27117

``docker-compose up -d``

To stop

``docker-compose stop``

To clean up everything after usage

``docker-compose down -v --rmi all --remove-orphans``

To use local server mongo server create database with you need
to change MONGO_PORT to the actual one (default in config is 27117)

***
### Run App
After db server ran we can start our application by running script:

``python run.py``

it will set up database and collection if they do not exist
***
### Api usage
db contains 1 collection for storing origins:
- allowed_origins - contains all added allowed origins. 
Note there additional checks for unique value

#### CORS middleware

Every method class of view is decorated with middleware 
checking 'Origin' header to be allowed. There present as decorators
both for view class and view method. In case if 'Origin' header 
does not present in request, middleware doing additional check 
on header 'Host' and allowing access if it's the same as server host.
#### hello world:
``GET http://localhost:8080/api/v1/index``


#### - Work with list of origins:
(use postman or equivalent requests in curl)

get list of all allowed origins

``GET http://localhost:8080/admin/allowed_origins``

add new origin to list

```
POST http://localhost:8080/admin/allowed_origins
body: {"origin": <origin_name>}
```

#### make preflight request
Make request on any endpoint with method OPTIONS and
receive list of allowed origins and methods for this endpoint.
If origin is not allowed, it will be handled by middleware and 
return status 403
