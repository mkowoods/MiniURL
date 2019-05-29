from flask import Flask, redirect
from flask_restful import Resource, Api, reqparse

import models
models.create_tables()

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('url')

class HealthCheck(Resource):
    def get(self):
        return {'status': 'ok'}

class HelloWorld(Resource):
    def get(self):
        return {'message': 'hello world'}

class URL(Resource):

    def get(self, key):
        if key == 'favicon.ico':
            return {'message': 'key not found'}, 404

        url = models.get_by_key(key)
        print("URL", url)
        if url:
            return {'url': url}
        return {'message': 'key not found'}, 404

    def delete(self, key):
        key = models.delete_by_key(key)
        return {'key': key}

class URLList(Resource):
    def get(self):
        return models.get_all_urls()

    def post(self):
        args = parser.parse_args()
        url = args['url']
        return models.add_url(url)

api.add_resource(HealthCheck, '/')
api.add_resource(HelloWorld, '/api/test')
api.add_resource(URLList, '/api/urls')
api.add_resource(URL, '/api/<string:key>')

if __name__ == '__main__':
    app.run("0.0.0.0", port=80, debug=True)
