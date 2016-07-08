# Simple API Proxy with Caching
A simple RESTful API Proxy written in Python/Flask that combines and caches multiple calls to an API into one single
call with a lightweight response. These kind of API Proxies are useful when creating a mobile application (in
order to send as little data as possible over the wire) or when combining multiple different APIs into one.


- [Table of contents](#table-of-contents)
	- [Prerequisites](#prerequisites)
	- [Setup](#setup)
	- [Dependencies](#dependencies)
	- [Available APIs](#available-apis)
		- [1. Events with subscriptions](#1-events-with-subscriptions)
	- [Executing Tests](#executing-tests)


## Prerequisites
 1. Python 3.2 or later.
 2. [virtualenv](https://virtualenv.pypa.io/en/stable/) is recommended.

## Setup
 1. Clone the repository using  
    `git clone https://github.com/ninadpdr/simple-api-proxy-cached.git`.
 2. This will create a new directory `simple-api-proxy-cached`.  
    From inside the directory, create a virtualenv using `virtualenv .venv`.
 3. Once the virtualenv is created, activate it using `source .venv/bin/activate`.
 4. Now, install all the packages from the `requirements.txt` file,  
    using the command, `pip install -r requirements.txt`.
 5. Then run the app using `python app.py`.  
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

#### 1. Events with subscriptions
Given an event ID, returns the event title and the first names of its attendees.

 - **URL**  
   `/events-with-subscriptions/:event_id` 
 - **Method**  
   `GET`
 - **URL Params**  
   **Required:**  
   `event_id=[string]`
 - **Data Params**  
   None
 - **Success Response**
	 - **Code:** 200 OK
	 - **Content:**  
       ```json
       {
           "id": "<event-id>",
           "title": "<event-title>",
           "names": "<list-of-first-names>"
       }
       ```
 - **Error Response**
	 - **Code:** 400 Bad Request, 502 Bad Gateway, 504 Gateway Timeout
	 - **Content:**  
       ```json
       {
           "error": {
               "message": "<error-description>", 
               "status_code": <HTTP-status-code>
           }
       }
       ```
 - **Sample Call**

   ```
   $ http GET http://0.0.0.0:5000/events-with-subscriptions/0069c02d7fa333a88b7e50d850b9bcf6_14677217380318/
   HTTP/1.0 200 OK
   Cache-Control: max-age=252
   Content-Length: 273
   Content-Type: application/json
   Date: Fri, 08 Jul 2016 18:43:05 GMT
   Server: Werkzeug/0.11.10 Python/3.5.1
   
   {
       "id": "0069c02d7fa333a88b7e50d850b9bcf6_14677217380318", 
       "names": [
           "API", 
           "Michel", 
           "Jasper", 
           "Bob", 
           "Dennis", 
           "Edmon", 
           "Aslesha", 
           "Lars"
       ], 
       "title": "Drink a cup of coffee with C42 Team"
   }
   
   $ http GET http://0.0.0.0:5000/events-with-subscriptions/0069c02d7fa333a88b7e50d850b9bcf6_1467721738031/
   HTTP/1.0 404 NOT FOUND
   Content-Length: 166
   Content-Type: application/json
   Date: Fri, 08 Jul 2016 18:43:11 GMT
   Server: Werkzeug/0.11.10 Python/3.5.1
   
   {
       "error": {
           "code": "NOT_FOUND", 
           "message": "Event 0069c02d7fa333a88b7e50d850b9bcf6_1467721738031 not found", 
           "status_code": 404
       }
   }
   ```

## Executing Tests
Tests are located under `tests` directory. To execute all tests,

 1. cd to project directory.
 2. `source .venv/bin/activate`.
 3. `python -m unittest discover -s tests`.
