from flask import Flask, request
import itertools

app = Flask(__name__)

datastore = {
   1 : {"task_name": "Task1", "difficulty": 3},
   2 : {"task_name": "Task2", "difficulty": 2},
   3 : {"task_name": "Task3", "difficulty": 1}
}

counter = itertools.count(3)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
   return datastore


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
   if id not in datastore.keys():
      return 'This ID does not exist'
   return datastore[id]


@app.route('/tasks', methods = ['POST'])
def create_new_task():
   content_type = request.headers.get('Content-Type')
   if (content_type == 'application/json'):
      data = request.json

      if (['task_name', 'difficulty'] == list(data.keys())):
         datastore[next(counter)] = data
         return data 
      else:
         return 'Not valid fields'
   else:
      return 'NOT JSON...'


@app.route('/tasks/<int:id>', methods = ['PUT'])
def update_task(id):
   if id not in datastore.keys():
      return 'This ID does not exist'

   content_type = request.headers.get('Content-Type')
   if (content_type == 'application/json'):
      data = request.json

      if (['task_name', 'difficulty'] == list(data.keys())):
         datastore[id] = data
         return data 
      else:
         return 'Not valid fields'
   else:
      return 'NOT JSON...'


@app.route('/tasks/<int:id>', methods = ['DELETE'])
def delete_task(id):
   if id not in datastore.keys():
      return 'This ID does not exist'
   return datastore.pop(id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
 
