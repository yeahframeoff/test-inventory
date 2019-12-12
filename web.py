from aiohttp import web

from Inventory import Inventory, load_inventory_from_file

async def get_categories_for_store(request):
    str_store_id = request.match_info.get('store_id')
    try:
        store_id = int(str_store_id)
    except ValueError:
        return web.json_response(
            {"error": "Please provide an integer as a store id"}, 
            status=400,
        )
    else:
        inventory = request.app["inventory"]
        result = inventory.get_categories_for_store(store_id)
        return web.json_response(result)

async def get_item_inventory(request):
    item_name = request.match_info.get('item_name')
    inventory = request.app["inventory"]
    result = inventory.get_item_inventory(item_name)
    return web.json_response(result)

async def get_median_for_category(request):
    str_category = request.match_info.get('category')
    try:
        category = int(str_category)
    except ValueError:
        return web.json_response(
            {"error": "Please provide an integer as a category id"},
            status=400,
        )
    else:
        inventory = request.app["inventory"]
        try:
            result = inventory.get_median_for_category(category)
        except ValueError:
            return web.json_response(
                {"error": "Cannot compute median for an empty category"},
                status=404,
            )
        else:
            return web.json_response(result)


app = web.Application()
app["inventory"] = Inventory(load_inventory_from_file("inventory.txt"))
app.add_routes([
    web.get('/get-categories-for-store/{store_id}', get_categories_for_store),
    web.get('/get-item-inventory/{item_name}', get_item_inventory),
    web.get('/get-median-for-category/{category}', get_median_for_category),
])

if __name__ == '__main__':
    web.run_app(app)