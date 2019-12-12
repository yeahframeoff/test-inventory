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
    
    def test_get_item_inventory(self, inventory):
        assert inventory.get_item_inventory("pc") == [
            {
                "store": 1,
                "category": 1,
                "item_name": "pc",
                "items":1,
                "price": 10
            },
            {
                "store": 2,
                "category": 1,
                "item_name": "pc",
                "items":3,
                "price": 3
            },
        ]

    def test_get_item_inventory(self, empty_inventory):
        assert empty_inventory.get_item_inventory("pc") == []
    
    def test_get_median_for_category_basic(self):
        items = [
            {
                "store": 1,
                "category": 1,
                "item_name": "The Item",
                "items": 4,
                "price": 200
            },
        ]

        inventory = Inventory(items)

        assert inventory.get_median_for_category(1) == 200
    
    def test_get_median_for_category_intermediate(self):
        items = [
            {
                "store": 1,
                "category": 1,
                "item_name": "The Item",
                "items": 4,
                "price": 200
            },
            {
                "store": 1,
                "category": 1,
                "item_name": "The Item Two",
                "items": 4,
                "price": 300
            },
        ]

        inventory = Inventory(items)

        assert inventory.get_median_for_category(1) == 250
    