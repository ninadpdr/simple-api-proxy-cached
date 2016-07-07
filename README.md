# Simple API Proxy with Caching
A simple API Proxy written in Python/Flask that combines and caches multiple calls to an API into one single
call with a lightweight response. These kind of API Proxies are useful when creating a mobile application (in
order to send as little data as possible over the wire) or when combining multiple different APIs into one.

[TOC]

## Prerequisites
 1. Python 3.2 or later.
 2. [virtualenv](https://virtualenv.pypa.io/en/stable/) is recommended.

## Setup
 1. Clone the repository using
    `git clone https://github.com/ninadpdr/simple-api-proxy-cached.git`
 2. This will create a new directory `simple-api-proxy-cached`.
    Inside the directory, create a virtualenv using `virtualenv .venv`
 3. Once the virtualenv is created, activate it using `source .venv/bin/activate`.
 4. Now, install all the packages from the `requirements.txt`
    file using the command, `pip install -r requirements.txt`
 5. Then run the app using `python app.py`
    This will start the API proxy server on http://0.0.0.0:5000/.

## Dependencies
This app uses following Python libraries:

 1. **[Flask](http://flask.pocoo.org/docs/0.11/)**
    This service is a perfect candidate for using a microframework. It's a simple RESTful web service, doesn't
    need ORM, templating, etc. Which is why Flask is chosen.
 2. **[Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.5/index.html)**
	Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs. Flask-RESTful
	encourages best practices with minimal setup. For example, we use using multiple return values in
	Flask-RESTful to return the response with an HTTP response status code.
 3. **[blinker](https://pythonhosted.org/blinker/)**
	This is a requirement for connecting a custom error handler to Flask-RESTful.
 4. **[requests](http://docs.python-requests.org/en/master/)**
    We use requests library to call the APIs we are proxying to.
 5. **[unittest](https://docs.python.org/3.5/library/unittest.html)**
    Test module in the Python standard library.
    
## Available APIs

### 1. Events with subscriptions
Returns event titles and the first names of its attendees.

 - **URL**
 - **Method**
 - **URL Params**
   **Required:**   
 - **Data Params**
 - **Success Response**
	 - **Code:** 200 OK
	 - **Content:**
        ```
        {
            "id": "<event-id>",
            "title": "<event-title>",
            "names": "<list-of-first-names>"
        }
        ```
 - **Error Response**
	 - **Code:** 400 Bad Request
	 - **Content:**
	    ```
        {
            "message": "<description>",
        }
        ```
 - **Sample Call**

## Executing Tests
Tests are located under `tests` directory. To execute all tests,

 1. cd to project directory
 2. `source .venv/bin/activate`
 3. `python -m unittest discover -s tests`
