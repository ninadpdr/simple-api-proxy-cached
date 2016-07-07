# encoding=utf-8
# Author: ninadpage

from flask_restful import Resource


class HelloWorld(Resource):
    """
    Endpoint to quickly check if the service is up.
    """

    def get(self):
        return "Hello, World!", 200
