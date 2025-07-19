from pathlib import Path

from app import ChatSearchEngine


def create_file(dir_path, name, content):
    path = Path(dir_path) / name
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def test_extract_metadata(tmp_path):
    file_path = create_file(tmp_path, 'sample.md', '---\naliases: Test\n---\nHello')
    engine = ChatSearchEngine(str(tmp_path))
    meta = engine.extract_metadata(file_path)
    assert meta['title'] == 'Test'
    assert meta['file_size'] > 0


def test_search_in_content():
    engine = ChatSearchEngine('.')
    match, positions = engine.search_in_content('Hello world', 'Hello', mode='ALL')
    assert match
    assert positions


def test_search(tmp_path):
    create_file(tmp_path, 'a.md', '# Title: First\nHello world')
    create_file(tmp_path, 'b.md', '# Title: Second\nAnother file')
    engine = ChatSearchEngine(str(tmp_path))
    query = {'terms': 'Hello', 'mode': 'ALL'}
    results = engine.search(query)
    assert len(results) == 1
    assert results[0]['title'] == 'First'
