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
                WHERE name LIKE '{child_name}'
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

    def remove_toy(self, child_name, toy_name):
        '''Removes a child's toy before it's delivered.'''

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(f'''
                    DELETE FROM Toys
                    WHERE child_id IN (
                        SELECT child_id FROM Toys
                        INNER JOIN Children ON Children.id = Toys.child_id
                        WHERE Children.name LIKE '{child_name}'
                    ) AND Toys.toy_name LIKE '{toy_name}'
                ''')
            except sqlite3.OperationalError as error:
                print("Error:", error)

    def find_toy(self, child_name, toy_name):
        '''Find a child's toy'''

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute(f'''
                SELECT id
                FROM Toys
                WHERE child_id IN (
                    SELECT child_id FROM Toys
                    INNER JOIN Children ON Children.id = Toys.child_id
                    WHERE Children.name LIKE '{child_name}'
                ) AND Toys.toy_name LIKE '{toy_name}'
            ''')
            toy = cursor.fetchone()

            # Returns tuple with ID, or None if not found
            return toy

    def list_gifts(self):
        '''Prints a list of children with gifts waiting to be delivered.'''

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT c.name, group_concat(t.toy_name, ', ') as toys
                FROM Children c
                JOIN Toys t ON t.child_id = c.id
                WHERE t.delivered == 0
                GROUP BY c.name
            ''')
            results = cursor.fetchall()

            if len(results) > 0:
                print('======== Gifts to be Delivered ========')
                for row in results:
                    print(row[0], ": ")
                    print(row[1], "\n")
            else:
                print('There are no gifts to be delivered')

    def list_gifts_single(self, child_name):
        """Prints the gifts to be delivered for a single child.

        Arguments:
            child_name {string} -- Child's name
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute(f'''
                SELECT c.name, group_concat(t.toy_name, ', ') as toys
                FROM Children c
                JOIN Toys t ON t.child_id = c.id
                WHERE t.delivered == 0 AND c.name LIKE '{child_name}'
            ''')

            result = cursor.fetchone()

            if result[0] is None:
                print("Child not found.")
            else:
                print(f"{result[0]}'s gifts: {result[1]}")


if __name__ == "__main__":
    lb = LootBag()
    if len(sys.argv) > 1:

        #add gift
        if sys.argv[1] == 'add':
            print('Add gift')
            toy_name = sys.argv[2]
            child_name = sys.argv[3]
            lb.add_toy(toy_name, child_name)
            print(f"{toy_name} added for {child_name}")

        #remove gift
        elif sys.argv[1] == 'remove':
            print('Remove')
            child_name = sys.argv[2]
            toy_name = sys.argv[3]
            lb.remove_toy(child_name, toy_name)

        #ls
        elif sys.argv[1] == 'ls':
            if(len(sys.argv) == 2):
                lb.list_gifts()
            else:
                lb.list_gifts_single(sys.argv[2])

        #delivered
        elif sys.argv[1] == 'delivered':
            print('Delivered')

        #help
        elif sys.argv[1] == 'help':
            print('help')

        else:
            print('You cannot do that! Type help.')
    else:
        print('Not enough arguments')
