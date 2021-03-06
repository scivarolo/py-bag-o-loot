import unittest
import string
import random

import sys
sys.path.append('../')
from lootbag import LootBag

def string_generator():
    '''Generates a random string for testing new entries in db.'''
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(7))

class TestLootBag(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.LootBag = LootBag()

    def test_find_child(self):
        '''Tests finding an existing child.'''
        child_name = "Elyse"
        self.assertEqual(self.LootBag.find_child(child_name), 1)

    def test_find_add_child(self):
        '''Tests adding a child when an existing child is not found.'''
        new_name = string_generator()
        self.assertIsInstance(self.LootBag.find_child(new_name), int)

    def test_add_toy_existing_child(self):
        '''Tests add a toy with existing child.'''
        child_name = "Elyse"
        toy_name = string_generator()

        self.assertIsInstance(self.LootBag.add_toy(toy_name, child_name), int)

    def test_add_toy_new_child(self):
        '''Tests add a toy with a new child.'''
        child_name = string_generator()
        toy_name = string_generator()

        self.assertIsInstance(self.LootBag.add_toy(toy_name, child_name), int)

    def test_remove_toy(self):
        '''Creates a toy, removes it, and checks it is gone.'''
        child_name = "Elyse"
        toy_name = string_generator()
        self.LootBag.add_toy(toy_name, child_name)
        self.LootBag.remove_toy(child_name, toy_name)
        self.assertIsNone(self.LootBag.find_toy(child_name, toy_name))

    def test_find_toy(self):
        '''Creates a child's toy in the database and then searches for it.'''
        child_name = string_generator()
        toy_name = string_generator()

        self.LootBag.add_toy(toy_name, child_name)
        self.assertIsInstance(self.LootBag.find_toy(child_name, toy_name), tuple)
        self.LootBag.remove_toy(child_name, toy_name)

    def test_list_gifts(self):
        '''Checks if a list of children is printed'''
        # Come back to this

    def test_list_gifts_single(self):
        '''Check if gifts for single child are printed.'''
        #come back to this

if __name__ == "__main__":
    unittest.main()
