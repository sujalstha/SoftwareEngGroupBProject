import pytest
import os
from db_checker import DBChecker  #

TEST_DB = "test_trivia_data.db"

@pytest.fixture()
def setup_temp_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_create_table_and_schema(setup_temp_db):
    db = DBChecker(TEST_DB)
    db.ensure_min_schema()
    assert db.table_exists()
    assert db.has_required_columns()


def test_insert_name_works(setup_temp_db):
    db = DBChecker(TEST_DB)
    db.ensure_min_schema()
    db.insert_name("Sujal")
    assert db.get_all_names() == ["Sujal"]


def test_empty_name_ignored(setup_temp_db):
    db = DBChecker(TEST_DB)
    db.ensure_min_schema()
    db.insert_name("")
    assert db.get_all_names() == []


def test_get_all_names_sorted(setup_temp_db):
    db = DBChecker(TEST_DB)
    db.ensure_min_schema()
    for name in ["Ryan", "Abraham", "Mo"]:
        db.insert_name(name)
    assert db.get_all_names() == ["Abraham", "Mo", "Ryan"]


def test_wipe_keeps_schema(setup_temp_db):
    db = DBChecker(TEST_DB)
    db.ensure_min_schema()
    db.insert_name("Jayce")
    assert db.get_all_names() == ["Jayce"]
    db.wipe()
    assert db.get_all_names() == []
    assert db.table_exists()
    assert db.has_required_columns()
