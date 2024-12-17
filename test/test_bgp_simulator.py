import unittest
from bgp_simulator import BGPSimulator

class TestBGPSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = BGPSimulator()

    def test_run_simulation(self):
        result = self.simulator.run_simulation()
        self.assertTrue(result, "Simulation should complete successfully")

    def test_handle_large_data(self):
        data = "x" * 10**6  # Simulating 1 MB of data
        processed = self.simulator.handle_large_data(data)
        self.assertTrue(processed, "Large data should be processed correctly")
