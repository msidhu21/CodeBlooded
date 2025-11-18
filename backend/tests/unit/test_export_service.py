from types import SimpleNamespace
import re
import pytest
from app.services.export_service import ExportService
from app.models.dto import ExportSelectionRequest
from app.core.errors import BadRequest


# Helper functions for creating test data
def make_item(item_id: int, sku: str = None, name: str = None, category: str = "c", 
              available: bool = True, description: str = "") -> SimpleNamespace:
    """Create a mock item for testing.
    
    Args:
        item_id: The item ID
        sku: Optional SKU (defaults to f"S{item_id}")
        name: Optional name (defaults to f"N{item_id}")
        category: Item category (default: "c")
        available: Availability status (default: True)
        description: Item description (default: "")
        
    Returns:
        SimpleNamespace object representing an item
    """
    return SimpleNamespace(
        id=item_id,
        sku=sku or f"S{item_id}",
        name=name or f"N{item_id}",
        category=category,
        available=available,
        description=description
    )


def make_items_for_ids(item_ids: list[int]) -> list[SimpleNamespace]:
    """Create a list of items for the given IDs.
    
    Args:
        item_ids: List of item IDs to create
        
    Returns:
        List of SimpleNamespace objects representing items
    """
    return [make_item(i) for i in item_ids]


# Fixtures
@pytest.fixture
def export_service():
    """Fixture providing an ExportService instance for testing."""
    return ExportService(db=None)


@pytest.fixture
def repo_factory():
    """Fixture providing a factory function to create fake repositories.
    
    Returns:
        Function that takes an items_func and returns a fake repo
    """
    def _make_fake_repo(items_func):
        """Create a fake repository that uses items_func to return items.
        
        Args:
            items_func: Function that takes a list of IDs and returns items
            
        Returns:
            Fake repository object with by_ids method
        """
        return type("FakeRepo", (), {"by_ids": lambda self, ids: items_func(ids)})()
    return _make_fake_repo


# Helper assertion functions
def assert_bad_request_with_ids(exc_info, expected_ids: list[int]) -> None:
    """Assert that a BadRequest exception contains the expected missing IDs.
    
    Args:
        exc_info: Exception info from pytest.raises context
        expected_ids: List of IDs that should be in the error message
    """
    detail = str(exc_info.value.detail)
    assert "Items not found" in detail
    for expected_id in expected_ids:
        assert str(expected_id) in detail


def assert_export_success(result, expected_count: int, expected_ids: list[int]) -> None:
    """Assert that an export result matches expectations.
    
    Args:
        result: ExportPayload result from export_selection
        expected_count: Expected count of items
        expected_ids: Expected list of item IDs in the result
    """
    assert result.count == expected_count
    assert len(result.items) == expected_count
    assert [item.id for item in result.items] == expected_ids


# Test cases
def test_export_selection_basic(export_service, repo_factory):
    """Test exporting a basic selection of items."""
    export_service.repo = repo_factory(lambda ids: [make_item(1), make_item(3)])
    result = export_service.export_selection(ExportSelectionRequest(ids=[1, 3]))
    assert_export_success(result, expected_count=2, expected_ids=[1, 3])


def test_export_selection_empty_list(export_service, repo_factory):
    """Test exporting with an empty ID list."""
    export_service.repo = repo_factory(lambda ids: [])
    result = export_service.export_selection(ExportSelectionRequest(ids=[]))
    assert result.count == 0
    assert result.items == []


def test_export_selection_single_item(export_service, repo_factory):
    """Test exporting a single item."""
    export_service.repo = repo_factory(lambda ids: [make_item(5)])
    result = export_service.export_selection(ExportSelectionRequest(ids=[5]))
    assert result.count == 1
    assert result.items[0].id == 5
    assert result.items[0].sku == "S5"


def test_export_selection_raises_for_missing_ids(export_service, repo_factory):
    """Test that BadRequest is raised when all requested IDs are missing."""
    export_service.repo = repo_factory(lambda ids: [])
    with pytest.raises(BadRequest) as exc_info:
        export_service.export_selection(ExportSelectionRequest(ids=[999, 1000]))
    assert_bad_request_with_ids(exc_info, [999, 1000])


def test_export_selection_raises_for_partial_missing(export_service, repo_factory):
    """Test that BadRequest is raised when some requested IDs are missing."""
    export_service.repo = repo_factory(lambda ids: [make_item(1)])
    with pytest.raises(BadRequest) as exc_info:
        export_service.export_selection(ExportSelectionRequest(ids=[1, 999, 1000]))
    assert_bad_request_with_ids(exc_info, [999, 1000])


def test_export_selection_returns_correct_count(export_service, repo_factory):
    """Test that export returns correct count for multiple items."""
    export_service.repo = repo_factory(lambda ids: make_items_for_ids(ids))
    result = export_service.export_selection(ExportSelectionRequest(ids=[1, 2, 3, 4, 5]))
    assert_export_success(result, expected_count=5, expected_ids=[1, 2, 3, 4, 5])


def test_export_selection_with_duplicate_ids(export_service, repo_factory):
    """Test exporting with duplicate IDs in the request.
    
    The service should handle duplicates by returning the item once per unique ID.
    """
    # Repository returns items for unique IDs only
    export_service.repo = repo_factory(lambda ids: make_items_for_ids(list(set(ids))))
    result = export_service.export_selection(ExportSelectionRequest(ids=[1, 1, 2, 2, 3]))
    # Should return 3 unique items
    assert result.count == 3
    assert sorted([item.id for item in result.items]) == [1, 2, 3]


def test_export_selection_mixed_valid_invalid_ids(export_service, repo_factory):
    """Test exporting with a mix of valid and invalid IDs.
    
    Should raise BadRequest with only the invalid IDs listed.
    """
    valid_ids = [1, 2, 3]
    invalid_ids = [999, 1000]
    export_service.repo = repo_factory(lambda ids: make_items_for_ids([i for i in ids if i in valid_ids]))
    
    with pytest.raises(BadRequest) as exc_info:
        export_service.export_selection(ExportSelectionRequest(ids=[1, 2, 3, 999, 1000]))
    
    # Should only report the invalid IDs
    assert_bad_request_with_ids(exc_info, invalid_ids)
    # Verify valid IDs are not in the error message by parsing the list
    detail = str(exc_info.value.detail)
    # Extract the list of IDs from the error message (format: "Items not found: [999, 1000]")
    match = re.search(r'\[([\d,\s]+)\]', detail)
    if match:
        reported_ids = [int(id_str.strip()) for id_str in match.group(1).split(',')]
        # Verify only invalid IDs are reported
        assert set(reported_ids) == set(invalid_ids)
        # Verify no valid IDs are in the reported list
        assert not any(valid_id in reported_ids for valid_id in valid_ids)

