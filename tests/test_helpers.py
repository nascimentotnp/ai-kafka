from pathlib import Path

from src.helpers import load, save


def test_save_and_load_file(tmp_path: Path):
    file_path = tmp_path / "ecomart.txt"
    content = "EcoMart - sustentabilidade ao seu alcance"

    ok = save(str(file_path), content)
    assert ok is True

    loaded = load(str(file_path))
    assert loaded == content
