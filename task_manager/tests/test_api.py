from datetime import datetime

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description",
        "priority": 2
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


def test_create_task_with_priority():
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description",
        "priority": 5
    })
    assert response.status_code == 422


def test_get_tasks():
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description",
        "priority": 2
    })
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = client.get("/tasks/")
    assert response.status_code == 200

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200


def test_get_tasks_with_page():
    response = client.get("/tasks/", params={
        "offset": 0,
        "limit": 10
    })
    assert response.status_code == 200


def test_get_tasks_with_sort():
    for i in ["priority", "due_date"]:
        response = client.get("/tasks/", params={
            "sort_by": i
        })
        assert response.status_code == 200


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task():
    # First create a task
    create_response = client.post("/tasks/", json={
        "title": "Update Test",
        "description": "Update Test描述",
        "priority": 2
    })
    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Title",
        "description": "Update Test Description",
        "priority": 2})
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Title"

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    update_response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Title",
        "description": "Update Test Description",
        "priority": 3})
    assert update_response.status_code == 404


def test_delete_task():
    # 创建任务
    create_response = client.post("/tasks/", json={
        "title": "Delete Test",
        "description": "Delete Test Description",
        "priority": 2})
    task_id = create_response.json()["id"]

    # 删除任务
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    # 验证任务已删除
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

    # 删除不存在的任务
    get_response_not_found = client.delete(f"/tasks/{task_id}")
    assert get_response_not_found.status_code == 404
