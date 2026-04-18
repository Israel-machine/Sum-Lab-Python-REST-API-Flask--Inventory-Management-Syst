import unittest
from lib.app import app

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_inventory(self):
        """Feature: View Inventory"""
        res = self.client.get("/inventory")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json, list)

    def test_create_product(self):
        """Feature: Manual Add"""
        payload = {"name": "Test Jam", "brands": "Test Brand", "price": 4.50}
        res = self.client.post("/inventory", json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json['name'], "Test Jam")

    def test_update_product(self):
        """Feature: Edit/Update Item (CRUD - Patch)"""
        payload = {"name": "Updated Coke", "price": 3.00}
        res = self.client.patch("/inventory/5449000000996", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['name'], "Updated Coke")

    def test_delete_product(self):
        """Feature: Delete Item"""
        res = self.client.delete("/inventory/3274080005003")
        self.assertEqual(res.status_code, 204)

    def test_fetch_external_api(self):
        """Feature: External API Integration (OpenFoodFacts)"""
        res = self.client.post("/inventory/fetch/3017620422003")
        self.assertIn(res.status_code, [201, 400])

if __name__ == "__main__":
    unittest.main()