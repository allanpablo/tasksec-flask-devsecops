def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json == {"status": "healthy"}


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"TaskSec" in resp.data


def test_register(client, auth):
    resp = auth.register()
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/auth/login")


def test_register_duplicate_username(client, auth):
    auth.register()
    resp = auth.register()
    assert resp.status_code == 200
    assert b"Este usu" in resp.data or b"j" in resp.data


def test_login_success(client, auth):
    auth.register()
    resp = auth.login()
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/dashboard")


def test_login_failure(client, auth):
    auth.register()
    resp = auth.login(password="wrongpass")
    assert resp.status_code == 200
    assert b"inv" in resp.data or b"erro" in resp.data


def test_logout(client, auth):
    auth.register()
    auth.login()
    resp = auth.logout()
    assert resp.status_code == 302


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Login" in resp.data or b"Entrar" in resp.data


def test_create_task(client, auth):
    auth.register()
    auth.login()
    resp = client.post("/task/create", data={"title": "Minha tarefa", "description": "Descricao"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Minha tarefa" in resp.data


def test_task_detail(client, auth):
    auth.register()
    auth.login()
    client.post("/task/create", data={"title": "Tarefa X"})
    resp = client.get("/task/1")
    assert resp.status_code == 200
    assert b"Tarefa X" in resp.data


def test_edit_task(client, auth):
    auth.register()
    auth.login()
    client.post("/task/create", data={"title": "Original"})
    resp = client.post("/task/1/edit", data={"title": "Editada", "completed": True}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Editada" in resp.data


def test_delete_task(client, auth):
    auth.register()
    auth.login()
    client.post("/task/create", data={"title": "Vai sumir"})
    resp = client.post("/task/1/delete", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Vai sumir" not in resp.data


def test_search(client, auth):
    auth.register()
    auth.login()
    client.post("/task/create", data={"title": "Comprar pao"})
    client.post("/task/create", data={"title": "Estudar python"})
    resp = client.get("/dashboard?q=pao")
    assert resp.status_code == 200
    assert b"Comprar pao" in resp.data
    assert b"Estudar python" not in resp.data
