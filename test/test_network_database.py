import unittest
from network_database import NetworkDatabase

class TestNetworkDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize the NetworkDatabase object
        self.db = NetworkDatabase()

    def test_connection(self):
        # Test the connection to the database
        connected = self.db.connect()
        self.assertTrue(connected, "Database should connect successfully")

    def test_insert_data(self):
        # Test inserting data into the database
        data = {"bandwidth": "1Gbps", "status": "active"}
        result = self.db.insert_data("network1", data)
        self.assertTrue(result, "Data should be inserted successfully")

    def test_retrieve_data(self):
        # Insert data and then retrieve it
        data = {"bandwidth": "1Gbps", "status": "active"}
        self.db.insert_data("network1", data)
        retrieved_data = self.db.retrieve_data("network1")
        self.assertEqual(retrieved_data["bandwidth"], "1Gbps", "Retrieved data should match")

    def test_update_data(self):
        # Insert data, update it, and check if the status is updated
        data = {"bandwidth": "1Gbps", "status": "active"}
        self.db.insert_data("network1", data)
        self.db.update_data("network1", "inactive")
        updated_data = self.db.retrieve_data("network1")
        self.assertEqual(updated_data["status"], "inactive", "Network status should be updated")

if __name__ == "__main__":
    unittest.main()
