import pytest

from web import create_app

@pytest.fixture
def cli(loop, aiohttp_client):
    app = create_app(inventory_file_path="inventory.txt")
    return loop.run_until_complete(aiohttp_client(app))


async def test_index_page_not_found(cli):
    resp = await cli.get('/')
    assert resp.status == 404


class TestGetCategoriesForStore:
    async def test_normal(self, cli):
        resp = await cli.get('/get-categories-for-store/1')
        assert resp.status == 200
        assert resp.content_type == "application/json"
        assert await resp.json() == [1, 2, 10]

    async def test_store_not_specified(self, cli):
        resp = await cli.get('/get-categories-for-store/')
        assert resp.status == 404

    async def test_store_non_integer(self, cli):
        resp = await cli.get('/get-categories-for-store/hello')
        assert resp.status == 400
        assert await resp.json() == {"error": "Please provide an integer as a store id"}
        assert resp.content_type == "application/json"


class TestGetItemInventory:
    async def test_normal(self, cli):
        resp = await cli.get('/get-item-inventory/pc')
        assert resp.status == 200
        assert resp.content_type == "application/json"
        assert await resp.json() == [
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
    
    async def test_item_name_not_specified(self, cli):
        resp = await cli.get('/get-item-inventory/')
        assert resp.status == 404
        

    async def test_item_does_not_exist(self, cli):
        resp = await cli.get('/get-item-inventory/mac')
        assert resp.status == 200
        assert resp.content_type == "application/json"
        assert await resp.json() == []


class TestGetMedianForCategory:
    async def test_normal(self, cli):
        resp = await cli.get('/get-median-for-category/1')
        assert resp.status == 200
        assert resp.content_type == "application/json"
        assert await resp.json() == 3
        assert await resp.text() == "3.0"
    
    async def test_category_not_specified(self, cli):
        resp = await cli.get('/get-median-for-category/')
        assert resp.status == 404
    
    async def test_category_non_integer(self, cli):
        resp = await cli.get('/get-median-for-category/hello')
        assert resp.status == 400
        assert await resp.json() == {"error": "Please provide an integer as a category id"}
    
    async def test_category_has_no_items(self, cli):
        # note that category #3 in our fixture file is not present
        resp = await cli.get('/get-median-for-category/3')
        assert resp.status == 404
        assert await resp.json() == {"error": "Cannot compute median for an empty category"}

