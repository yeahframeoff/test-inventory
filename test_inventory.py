from Inventory import load_inventory_from_file, Inventory

import pytest

@pytest.fixture
def items():
    return load_inventory_from_file("inventory.txt")

@pytest.fixture
def inventory(items):
    return Inventory(items)

@pytest.fixture
def empty_inventory():
    return Inventory([])

class TestInventory:
    def test_empty_inventory_is_allowed(self):
        inventory = Inventory([])
    
    def test_get_categories_for_store(self, inventory):
        assert inventory.get_categories_for_store(1) == [1, 2, 10]
        
        assert inventory.get_categories_for_store(2) == [1, 10]
        
        assert inventory.get_categories_for_store(3) == [120]

        assert inventory.get_categories_for_store(4) == []

        assert inventory.get_categories_for_store(30) == [2]
    
    def test_get_categories_for_store_in_empty_inventory(self, empty_inventory):
        assert empty_inventory.get_categories_for_store(1) == []
