-- Insert sample data into the network_configurations table
USE vajra_network;

INSERT INTO network_configurations (network_name, bandwidth, status)
VALUES
    ('network1', '1Gbps', 'active'),
    ('network2', '10Gbps', 'inactive'),
    ('network3', '100Mbps', 'active');

-- Insert sample data into billing_records table
INSERT INTO billing_records (user_id, amount, payment_status)
VALUES
    (1, 99.99, 'Completed'),
    (2, 149.99, 'Pending');
