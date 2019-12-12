#!/usr/bin/env python3
import json
from statistics import median

from itertools import chain, repeat

class Inventory:
    """
    Inventory Management system 
    """

    def __init__(self, items):
        self.items = items

    def _filter_items_by(self, predicate):
        return list(filter(predicate, self.items))
    
    def get_categories_for_store(self, store):
        """
        Given a store id you should return all the categories ids in the inventory.
        :param store: store id
        :return: all the categories ids in the inventory
        """
        pred = lambda item: item["store"] == store
        items =  self._filter_items_by(pred)

        return sorted(set(item["category"] for item in items))

    def get_item_inventory(self, item_name):
        """
        Given items name return all the items across all stores.
        :param item_name: item name
        :return: all the items across all stores
        """
        pred = lambda item: item["item_name"] == item_name
        return self._filter_items_by(pred)

    def get_median_for_category(self, category):
        """
        Given category id return the median of the prices for all items in the category.
        :param category: category name
        :return: the median of the prices for all items in the category
        """
        pred = lambda item: item["category"] == category
        items_in_category = self._filter_items_by(pred)

        if not items_in_category:
            raise ValueError("Cannot find median for category with no items")

        prices_and_counts = (
            (item["price"], item["items"]) 
            for item in items_in_category
        )

        all_prices = chain.from_iterable(
            repeat(price, count)
            for price, count in prices_and_counts
        )
        
        return median(all_prices)


def load_inventory_from_file(file_name):
    with open(file_name) as fp:
        return json.load(fp)
