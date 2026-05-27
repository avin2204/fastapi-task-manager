from .conftest import client


def get_token():

    login_response = client.post(
        "/login",
        json={
            "email": "avin@test.com",
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    return token


def test_create_task():

    token = get_token()

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "pytest task",
            "description": "testing task",
            "priority": "high"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Task created successfully"


def test_get_tasks():

    token = get_token()

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_update_task():

    token = get_token()

    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "old task",
            "description": "old description",
            "priority": "medium"
        }
    )

    task_id = create_response.json()["task_id"]

    response = client.put(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "updated task",
            "description": "updated description",
            "status": "completed",
            "priority": "high"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Task updated successfully"


def test_delete_task():

    token = get_token()

    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "delete task",
            "description": "delete description",
            "priority": "low"
        }
    )

    task_id = create_response.json()["task_id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Task deleted successfully"