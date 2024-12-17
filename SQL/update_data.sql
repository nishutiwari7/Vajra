-- Update status for a network configuration
USE vajra_network;

UPDATE network_configurations
SET status = 'inactive'
WHERE network_name = 'network1';
