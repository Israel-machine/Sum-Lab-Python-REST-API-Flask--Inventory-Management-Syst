import unittest
from lib.app import app

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_inventory(self):
        """Scenario: View Inventory (Dynamic)"""
        res = self.client.get("/inventory")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json, list)

    def test_create_product(self):
        """Scenario: Manual Add (Dynamic)"""
        payload = {"name": "Dynamic Apple", "brands": "Nature", "price": 0.99}
        res = self.client.post("/inventory", json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json['name'], "Dynamic Apple")
        self.assertIn('code', res.json) # Verify a code was generated automatically

    def test_update_product(self):
        """Scenario: Edit/Update Item (Dynamic)"""
        create_res = self.client.post("/inventory", json={
            "name": "Original Name", 
            "brands": "BrandX", 
            "price": 1.0
        })
        item_id = create_res.json['code']
        patch_payload = {"name": "Refactored Name", "price": 5.50}
        res = self.client.patch(f"/inventory/{item_id}", json=patch_payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['name'], "Refactored Name")
        self.assertEqual(res.json['price'], 5.50)

    def test_delete_product(self):
        """Scenario: Delete Item (Dynamic)"""
        create_res = self.client.post("/inventory", json={
            "name": "Ephemeral Item", 
            "brands": "None", 
            "price": 0.0
        })
        item_id = create_res.json['code']
        res = self.client.delete(f"/inventory/{item_id}")
        self.assertEqual(res.status_code, 204)
        check_res = self.client.get(f"/inventory/{item_id}")
        self.assertEqual(check_res.status_code, 404)

    def test_fetch_external_api(self):
        """Scenario: External API Integration (Dynamic)"""
        barcode = "3017620422003"
        res = self.client.post(f"/inventory/fetch/{barcode}")
        self.assertIn(res.status_code, [201, 400])
        if res.status_code == 201:
            self.assertEqual(res.json['code'], barcode)

if __name__ == "__main__":
    unittest.main()