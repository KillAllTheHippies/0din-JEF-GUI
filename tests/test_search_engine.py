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


def test_search_folder_filters(tmp_path):
    folder_a = tmp_path / 'a'
    folder_a.mkdir()
    folder_b = tmp_path / 'b'
    folder_b.mkdir()

    create_file(folder_a, 'file1.md', 'Hello world')
    create_file(folder_b, 'file2.md', 'Hello world')

    engine = ChatSearchEngine(str(tmp_path))

    query_included = {
        'terms': 'Hello',
        'mode': 'ALL',
        'includedFolders': ['a']
    }
    results_included = engine.search(query_included)
    assert len(results_included) == 1
    assert results_included[0]['path'].startswith('a/')

    query_excluded = {
        'terms': 'Hello',
        'mode': 'ALL',
        'excludedFolders': ['a']
    }
    results_excluded = engine.search(query_excluded)
    assert len(results_excluded) == 1
    assert results_excluded[0]['path'].startswith('b/')


def test_search_in_content_any_case(tmp_path):
    engine = ChatSearchEngine(str(tmp_path))
    match, positions = engine.search_in_content('Foo Bar', 'bar', mode='ANY', case_sensitive=False)
    assert match
    assert positions
