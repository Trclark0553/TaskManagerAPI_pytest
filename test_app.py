import pytest
from run import app, tasks

# Fixture to create a test client for making requests to the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True #Enable test mode for better error messages
    with app.test_client() as client:
        tasks.clear() # Clear tasks before each test
        yield client 

# Smoke Test: Home route returns 200 OK and correct message
@pytest.mark.smoke 
def test_home(client):
    """Verify that home page is reachable and displays correct message."""
    response = client.get('/') # Send GET request to home
    assert response.status_code == 200, "Expected 200 OK status code" #HTTP good
    assert b"Task Manager API is running..." in response.data # Verify welcome test in body

# Smoke Test: Tasks returns an empty list initially
@pytest.mark.smoke 
def test_get_empty_tasks(client):
    """Verify that /tasks initially returns an empty list."""
    response = client.get('/tasks')
    assert response.status_code == 200, "Expected 200 OK status code" #HTTP good
    assert response.get_json() == [], "Expected empty list of tasks" #Empty list

# Regression Test: Creating new task is added to list
@pytest.mark.regression
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

# Regression Test: Deleteing a task removes it from the list
@pytest.mark.regression
def test_delete_task(client):
    """Verify that DELETE /tasks/<id> removes it from teh list"""
    # Create a task to delete
    client.post('/tasks', json={"title": "Do Laundry"})

    # Delete it
    response = client.delete('/tasks/1')
    assert response.status_code == 200 #HTTP success

    # Verify list is empty after
    response = client.get('/tasks')
    assert response.get_json() == []

# Regression Test: Deleting a non-existent task returns 404
@pytest.mark.regression
def test_delete_non_existent_task(client):
    """Verify that deleting a non-existent task returns 404"""
    response = client.delete('/tasks/999') # task 999 does not exist
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task 999 not found." #Error msg