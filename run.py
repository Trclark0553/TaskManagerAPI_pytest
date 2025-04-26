from flask import Flask, jsonify #import jsonify, flask function that converts python data to JSON

app = Flask(__name__)

tasks = [] #instantiate task dictionary

@app.route('/') #home endpoint
def home():
    return "Task Manager API is running..."

@app.route('/tasks', methods=['GET']) #tasks endpoint, returns tasks in JSON
def get_tasks():
    return jsonify(tasks), 200 

if __name__ == '__main__':
    app.run(debug=True)