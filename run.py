from flask import Flask, jsonify, request #jsonify, flask function that converts python data to JSON

app = Flask(__name__)

tasks = [] #instantiate task dictionary
next_id = 1 # task counter

# Root endpoint
@app.route('/')
def home():
    return "Task Manager API is running..."

# GET /tasks: Returns tasks as JSON
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200 #successful request

# POST /tasks: Creates new tasks from JSON formatted input
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json() # get json from request

    # Validate 'title' is given
    if not data or 'title' not in data:
        return jsonify({"error" : "Task title is required"}), 400 #bad request

    # Create task and add to list
    task = {"id": next_id, "title": data["title"]}
    tasks.append(task)
    next_id += 1 #Increment id for next task

    return jsonify(task), 201 #resource created

# DELETE /tasks/task_id. Ex: curl -x delete http://localhost:5000/tasks/1
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks

    #loop through list to find first match, if not found set default=None
    task = next((t fo t in tasks if t["id"] == task_id), None)

    #report to user task not found, return 404
    if not task:
        return jsonify({"error": "Task not found"}), 404

    #modify list to exclude target task id
    tasks = [t for t in tasks if t["id"] != task_id]

    return '', 204


if __name__ == '__main__':
    app.run(debug=True)