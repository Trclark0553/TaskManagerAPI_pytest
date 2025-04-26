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


if __name__ == '__main__':
    app.run(debug=True)