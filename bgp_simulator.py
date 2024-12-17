from netmiko import ConnectHandler
import logging

# Setup logging for the output
logging.basicConfig(level=logging.INFO)

def update_bgp_configuration():
    try:
        # Define device connection parameters
        device = {
            'device_type': 'cisco_ios',  # Change this based on your device type (e.g., juniper, arista)
            'host': '192.168.1.1',       # IP address of your device
            'username': 'admin',         # SSH username
            'password': 'password',      # SSH password
            'secret': 'secret',          # Privileged mode password (if needed)
            'port': 22,                  # SSH port (default is 22)
            'timeout': 30,               # Timeout for connection
        }

        # Establish an SSH connection to the network device
        logging.info(f"Connecting to {device['host']}...")
        net_connect = ConnectHandler(**device)
        net_connect.enable()  # Enter enable mode (privileged mode)

        # Define the BGP configuration commands
        config_commands = [
            'router bgp 65000',              # Enter BGP configuration mode for ASN 65000
            'neighbor 192.168.2.1 remote-as 65001',  # Set neighbor 192.168.2.1 with remote AS 65001
            'network 192.168.0.0 mask 255.255.255.0', # Announce a network
            'exit',  # Exit BGP configuration mode
        ]

        # Send the configuration commands to the device
        logging.info("Sending BGP configuration commands...")
        output = net_connect.send_config_set(config_commands)

        # Output the results of the configuration change
        logging.info("Configuration update successful. Output:")
        logging.info(output)

        # Save the configuration (optional)
        logging.info("Saving the configuration...")
        net_connect.save_config()

        # Disconnect the session
        net_connect.disconnect()
        logging.info(f"Disconnected from {device['host']}")

    except Exception as e:
        logging.error(f"Error during BGP configuration update: {e}")

if __name__ == "__main__":
    update_bgp_configuration()
