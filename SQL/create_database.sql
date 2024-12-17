-- Create a new database for the Vajra project
CREATE DATABASE IF NOT EXISTS vajra_network;

USE vajra_network;

-- Create table for network configurations
CREATE TABLE IF NOT EXISTS network_configurations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    network_name VARCHAR(255) NOT NULL,
    bandwidth VARCHAR(255),
    status VARCHAR(255) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table for billing records
CREATE TABLE IF NOT EXISTS billing_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
