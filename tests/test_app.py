def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json == {"status": "healthy"}


def test_about_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Task Manager" in resp.data


def test_register(client, auth):
    resp = auth.register()
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")


def test_register_duplicate_username(client, auth):
    auth.register()
    resp = auth.register()
    assert resp.status_code == 200
    assert b"Username Exists" in resp.data


def test_login_success(client, auth):
    auth.register()
    resp = auth.login()
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/all_tasks")


def test_login_failure(client, auth):
    auth.register()
    resp = auth.login(password="wrongpass")
    assert resp.status_code == 200
    assert b"Login Unsuccessful" in resp.data


def test_logout(client, auth):
    auth.register()
    auth.login()
    resp = auth.logout()
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")


def test_all_tasks_requires_login(client):
    resp = client.get("/all_tasks", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Login" in resp.data


def test_create_task(client, auth):
    auth.register()
    auth.login()
    resp = client.post(
        "/add_task", data={"task_name": "Minha tarefa"}, follow_redirects=True
    )
    assert resp.status_code == 200
    assert b"Task Created" in resp.data

    resp = client.get("/all_tasks")
    assert b"Minha tarefa" in resp.data


def test_update_task(client, auth):
    auth.register()
    auth.login()
    client.post("/add_task", data={"task_name": "Original"})
    resp = client.post(
        "/all_tasks/1/update_task",
        data={"task_name": "Editada"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Editada" in resp.data


def test_delete_task(client, auth):
    auth.register()
    auth.login()
    client.post("/add_task", data={"task_name": "Vai sumir"})
    resp = client.get("/all_tasks/1/delete_task", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Vai sumir" not in resp.data


def test_user_cannot_update_other_users_task(client, auth):
    auth.register(username="userone")
    auth.login(username="userone")
    client.post("/add_task", data={"task_name": "Privada"})
    auth.logout()

    auth.register(username="usertwo")
    auth.login(username="usertwo")
    resp = client.get("/all_tasks/1/update_task")
    assert resp.status_code == 403
