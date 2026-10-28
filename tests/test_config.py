from src import config


def test_default_key_is_set():
    assert config.DEFAULT_KEY_COLUMN == "id"
