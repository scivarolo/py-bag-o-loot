import sqlite3
import sys

maindb = '/Users/sebastiancivarolo/workspace/python/exercises/bagoloot/db.db'

class LootBag:

    def __init__(self, db=maindb):
        self.db = db

    def add_toy(self, toy_name, child_name):
        ''' Adds a toy to the database.

            Arguments:
                toy_name - string
                child_name - string

            Returns:
                int - ID of child
        '''

        # Check if child exists in database, or create child
        child_id = self.find_child(child_name)

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO Toys VALUES (?, ?, ?, ?)
            ''', (None, toy_name, child_id, 0))

            return cursor.lastrowid

    def find_child(self, child_name):
        ''' Queries the Children table to see if a child exists.
            If a child doesn't exist, it is created.

            Arguments:
                child_name - String

            Returns:
                int - ID of child
        '''

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            # Search DB for child
            cursor.execute(f'''
                SELECT id
                FROM Children
                WHERE name = '{child_name}'
            ''')

            child_id = cursor.fetchone()

            if child_id != None:
                return child_id[0]
            else:
                # create child
                return self.create_child(child_name)

    def create_child(self, child_name):
        ''' Creates a new child in the database.

            Arguments:
                child_name - String

            Returns:
                int - ID of new child
        '''

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO Children VALUES (?, ?)
            ''', (None, child_name))

            return cursor.lastrowid
