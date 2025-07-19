import app


def test_get_settings_endpoint(tmp_path):
    app.config.set("archive_path", str(tmp_path))
    client = app.app.test_client()
    response = client.get('/api/settings')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "archive_path" in data


def test_validate_archive_path_endpoint(tmp_path):
    client = app.app.test_client()
    payload = {"path": str(tmp_path)}
    response = client.post('/api/validate-archive-path', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["valid"]
    assert data["file_count"] == 0
