import pytest
from app import app

# Fixture to create a test client for making requests to the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True #Enable test mode for better error messages
    with app.test_client() as client:
        yield client 

# Test: Home route returns 200 OK and correct message
def test_home(client):
    """Verify that home page is reachable and displays correct message."""
    response = client.get('/') # Send GET request to home
    assert response.status_code == 200 # Verify HTTP response
    assert b"Task Manager API is running..." in response.data # Verify welcome test in body

# Test: Tasks returns an empty list initially
def test_get_empty_tasks(client):
    """Verify that /tasks initially returns an empty list."""
    response = client.get('/tasks')
    assert response.status_code = 200 #HTTP good
    assert response.get_json() == [] #assume empty list

# Test: Creating new task is added to list
def test_create_task(client):
    """Verify that POST /tasks creates a new tASK"""
    task_data= {"title": "Buy groceries"}
    response = client.post('/tasks', json=task_data)
    assert response.status_code == 201 #HTTP create success
    new_task = response.get_json()
    assert new_task["id"] == 1 #Test first task id = 1
    assert new_task["title"] == "Buy groceries" #Add task

    #Verify tasks appears in the task list
    response = client.get('/tasks')
    tasks_list = response.get_json()
    assert len(tasks_list) == 1 #Test length is 1
    assert tasks_list[0]["title"] == "Buy groceries" #Test task added correctly