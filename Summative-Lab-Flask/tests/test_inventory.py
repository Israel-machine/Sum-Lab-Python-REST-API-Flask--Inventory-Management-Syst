import unittest
from lib.app import app

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_inventory(self):
        res = self.client.get("/inventory")
        self.assertEqual(res.status_code, 200)

    def test_create_product(self):
        payload = {"name": "Test", "brands": "Brand", "price": 1.0}
        res = self.client.post("/inventory", json=payload)
        self.assertEqual(res.status_code, 201)

    def test_delete_product(self):
        # Use an ID from your data.py
        res = self.client.delete("/inventory/3274080005003")
        self.assertEqual(res.status_code, 204)

if __name__ == "__main__":
    unittest.main()