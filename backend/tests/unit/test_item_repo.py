import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.repos.item_repo import ItemRepo
from app.models.entities import Base, Item

@pytest.fixture
def db_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def repo(db_session):
    return ItemRepo(db_session)

@pytest.fixture
def sample_items(repo):
    items = [
        Item(sku="SKU1", name="Item 1", category="tools", available=True, description=""),
        Item(sku="SKU2", name="Item 2", category="tools", available=True, description=""),
        Item(sku="SKU3", name="Item 3", category="tools", available=True, description=""),
    ]
    for item in items:
        repo.db.add(item)
    repo.db.commit()
    return items

def test_by_ids_returns_matching_items(repo, sample_items):
    result = repo.by_ids([1, 3])
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3

def test_by_ids_returns_empty_list_for_empty_input(repo):
    result = repo.by_ids([])
    assert result == []

def test_by_ids_returns_only_existing_items(repo, sample_items):
    result = repo.by_ids([1, 999, 2])
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

def test_by_ids_returns_empty_for_nonexistent_ids(repo):
    result = repo.by_ids([999, 1000])
    assert result == []

