from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

IMAGES = {
    'input': '/Users/joeybose/Desktop/hackathon/images',
    'output': 'output directory',
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in IMAGES:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Image(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return IMAGES[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del IMAGES[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = args['task']
        IMAGES[todo_id] = task
        return task, 201

# ImageList
# shows a list of all IMAGES, and lets you POST to add new tasks
class ImageList(Resource):
    def get(self):        
        return IMAGES

class Home(Resource):
    def get(self):        
        return IMAGES

##
## Actually setup the Api resource routing here
##
api.add_resource(ImageList, '/images')
api.add_resource(Image, '/images/<todo_id>')
api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)