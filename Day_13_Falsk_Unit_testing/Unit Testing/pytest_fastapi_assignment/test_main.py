from pydoc import resolve

from fastapi.testclient import TestClient
from main import app

client=TestClient(app)

def test_get_tasks():
    response=client.get("/tasks")
    assert response.status_code==200

def test_get_tasks_return_list():
    response=client.get("/tasks")
    assert isinstance(response.json(),list)

def test_get_task_id():
    response=client.get("/tasks/1")

    assert response.status_code==200
    data=response.json()
    assert data["id"] == 1

def test_get_task_id_not_meet():
    response=client.get("/tasks/999")

    assert response.status_code==404


def test_add_task():
    response=client.post("/tasks",
                         json={
                              "id": 4,
                            "title": "Check server logs",
                                "status": "Pending"
    })

    assert response.status_code==200

    data=response.json()

    assert data["id"] == 4
    assert data["title"] == "Check server logs"
    assert data["status"] == "Pending"

def test_invalid_task():
    response=client.post("/tasks",
                         json={
                             "id": 4,
                             "title": "Check server logs"
                             # status
                         })
    assert response.status_code==422


def test_update_task_status():
    response=client.put("/tasks/2",
                        json={
                         "id": 2,
                        "title": "Review invoice",
                         "status": "Completed"
                        })
    assert response.status_code==200
    data=response.json()
    assert data["id"] == 2
    assert data["status"] == "Completed"

def test_delete_tasks():
    response=client.delete("/tasks/3")
    assert response.status_code==200
    data=response.json()
    assert data["id"] == 3



# python -m pytest -v



