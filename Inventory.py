#!/usr/bin/env python3
import json
from statistics import median

from itertools import chain

class Inventory(object):
    """
    Inventory Management system 
    """

    def __init__(self):
        with open("inventory.txt") as fp:
            self.items = json.load(fp)
    
    def get_categories_for_store(self, store):
        """
        Given a store id you should return all the categories ids in the inventory.
        :param store: store id
        :return: all the categories ids in the inventory
        """
        return list(filter(lambda item: item["store"] == store, self.items))
    def get_item_inventory(self, item_name):
        """
        Given items name return all the items across all stores.
        :param item_name: item name
        :return: all the items across all stores
        """
        return list(filter(lambda item: item["item_name"] == item_name, self.items))
    def get_median_for_category(self, category):
        """
        Given category id return the median of the prices for all items in the category.
        :param category: category name
        :return: the median of the prices for all items in the category
        """
        items_in_category = filter(lambda item: item["category"] == category, self.items)

        all_prices = chain.from_iterable([item["price"]] * item["items"] for item in items_in_category)
        return median(all_prices)
