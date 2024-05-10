# import unittest
# import requests
# import json

import unittest
from fastapi.testclient import TestClient
from main import app # Asegúrate que esta importación es correcta según tu estructura de proyecto

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def testreadroot(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("welcome", response.json())

    def testsearch_by_id_success(self):
        response = self.client.get("/search/1")  # Asumiendo que el ID 1 existe
        self.assertEqual(response.status_code, 200)

    def test_search_by_id_failure(self):
        response = self.client.get("/search/999")  # Asumiendo que el ID 999 no existe
        self.assertEqual(response.status_code, 200)

    def test_get_all_search_success(self):
        response = self.client.get("/searchs")
        self.assertEqual(response.status_code, 200)

    def test_get_budget_id_success(self):
        response = self.client.get("/budget/1")  # Asumiendo que el ID 1 existe
        self.assertEqual(response.status_code, 200)

    def test_get_budget_id_failure(self):
        response = self.client.get("/budget/999")  # Asumiendo que el ID 999 no existe
        self.assertEqual(response.status_code, 200)

    def test_get_all_contacts(self):
        response = self.client.get("/contacts")
        self.assertEqual(response.status_code, 200)

    def test_post_search(self):
        search_data = {"prompt": "example prompt"}
        response = self.client.post("/search", json=search_data)
        self.assertEqual(response.status_code, 201)

    def test_post_contact(self):
        contact_data = {"name": "John Doe", "email": "john@example.com", "type_of": "type1", "state": 1, "decision": 0}
        response = self.client.post("/contact", json=contact_data)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()