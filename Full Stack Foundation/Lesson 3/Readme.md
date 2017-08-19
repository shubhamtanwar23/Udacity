# Flask Framework

[Flask](http://flask.pocoo.org/) is a micro web framework written in Python and based on the Werkzeug toolkit and Jinja2 template engine. It is BSD licensed.
Flask is called a micro framework because it does not require particular tools or libraries. 
It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. 
However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools.

### Installation

[Steps to Install](http://flask.pocoo.org/docs/0.12/installation/) - Official website

# Working of site

### Database
[SQLite3](https://www.sqlite.org/) is used for data storage i.e different Restaurant names and their menus.

### Backend Implementation
[Flask](http://flask.pocoo.org/) framework is used for implementing a server to handle a the request generated. It is able to perform the following http requests
* GET
* POST

### API Endpoints
API endpoints are created to send the data to a third applictaion in [JSON](www.json.org/) format. 
