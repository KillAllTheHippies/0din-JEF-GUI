import json
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


def test_reset_settings_endpoint(tmp_path):
    app.config.config_file = tmp_path / "settings.json"
    client = app.app.test_client()
    response = client.post('/api/settings/reset')
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"]


def test_export_settings_endpoint(tmp_path):
    app.config.config_file = tmp_path / "settings.json"
    app.config.set("archive_path", str(tmp_path))
    client = app.app.test_client()
    response = client.get('/api/settings/export')
    assert response.status_code == 200
    assert response.mimetype == 'application/json'


def test_import_settings_endpoint(tmp_path):
    app.config.config_file = tmp_path / "settings.json"
    app.config.set("archive_path", str(tmp_path))
    export_path = tmp_path / "export.json"
    app.config.export_settings(str(export_path))

    new_path = tmp_path / "new"
    new_path.mkdir()
    with open(export_path, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['archive_path'] = str(new_path)
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    client = app.app.test_client()
    with open(export_path, 'rb') as f:
        data = {'file': (f, 'settings.json')}
        response = client.post('/api/settings/import', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    resp_data = response.get_json()
    assert resp_data['success']
    assert app.config.get('archive_path') == str(new_path)
