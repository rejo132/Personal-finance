import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from lib.db import Session
from lib.helpers import create_user, list_users, create_category, create_transaction
from lib.db.models import User, Category

class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.session.query(User).delete()
        self.session.query(Category).delete()
        self.session.commit()

    def test_create_user(self):
        user = create_user(self.session, "testuser", "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        with self.assertRaises(ValueError):
            create_user(self.session, "testuser", "test2@example.com")

    def test_list_users(self):
        create_user(self.session, "testuser", "test@example.com")
        users = list_users(self.session)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, "testuser")

    def test_create_category(self):
        create_user(self.session, "testuser", "test@example.com")
        category = create_category(self.session, "testuser", "Food")
        self.assertEqual(category.name, "Food")
        with self.assertRaises(ValueError):
            create_category(self.session, "testuser", "Food")

    def test_create_transaction(self):
        create_user(self.session, "testuser", "test@example.com")
        create_category(self.session, "testuser", "Food")
        transaction = create_transaction(
            self.session, "testuser", 50.0, "expense", "Food", "Groceries", "2025-05-26"
        )
        self.assertEqual(transaction.amount, 50.0)
        self.assertEqual(transaction.type, "expense")
        with self.assertRaises(ValueError):
            create_transaction(
                self.session, "testuser", 50.0, "expense", "Travel", "Invalid", "2025-05-26"
            )

    def tearDown(self):
        self.session.rollback()
        self.session.close()

if __name__ == '__main__':
    unittest.main()