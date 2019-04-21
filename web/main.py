from flask import Flask, redirect
from flask_restful import Resource, Api, reqparse

import models

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('url')

class HelloWorld(Resource):
    def get(self):
        return {'message': 'hello world'}

class URL(Resource):

    def get(self, key):
        if key == 'favicon.ico':
            return {'message': 'key not found'}, 404

        url = models.get_by_key(key)
        if url:
            return redirect(url, code=302)
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
        return models.add_url(url), 201


api.add_resource(HelloWorld, '/hw')
api.add_resource(URLList, '/urls')
api.add_resource(URL, '/<string:key>')

if __name__ == '__main__':
    app.run("0.0.0.0", port=80, debug=True)
