import requests
import logging
from datetime import datetime

class IXPManager:
    def __init__(self):
        self.ixp_status = {}  # Cache for IXP status

    def access_ixp(self, network_id):
        """Access an IXP for the given network."""
        logging.info(f"Attempting to access IXP for network: {network_id}")
        if network_id in self.ixp_status and self.ixp_status[network_id] == "accessed":
            raise Exception(f"Network {network_id} has already accessed the IXP.")

        self.ixp_status[network_id] = "accessed"
        logging.info(f"Successfully accessed IXP for network: {network_id}")
        return True

    def monitor_ixps(self, ixp_list):
        """Monitor IXP statuses in real-time."""
        logging.info("Starting IXP monitoring...")
        for ixp in ixp_list:
            try:
                response = requests.get(f"http://ixp_api/{ixp}/status")
                if response.status_code == 200:
                    self.ixp_status[ixp] = response.json().get("status", "unknown")
                    logging.info(f"IXP {ixp} status updated: {self.ixp_status[ixp]}")
            except requests.RequestException as e:
                logging.error(f"Error fetching IXP status for {ixp}: {e}")

    def prioritize_access(self, ixp_list):
        """Prioritize networks based on IXP load and availability."""
        sorted_ixps = sorted(ixp_list, key=lambda ixp: self.ixp_status.get(ixp, "unknown"))
        logging.info(f"Prioritized IXP access: {sorted_ixps}")
        return sorted_ixps
