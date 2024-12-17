import os
import shutil
import logging
from datetime import datetime, timedelta
import mysql.connector
import psycopg2
from config import DATABASE_URI


class NetworkDatabase:
    def __init__(self, db_type="mysql", host="localhost", user="root", password="password", database="vajra_network"):
        """
        Initialize the database connection.
        :param db_type: Type of the database ('mysql' or 'postgresql')
        :param host: Database host (MySQL or PostgreSQL)
        :param user: Database username
        :param password: Database password
        :param database: Database name
        """
        self.db_type = db_type
        if self.db_type == "mysql":
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
        elif self.db_type == "postgresql":
            self.conn = psycopg2.connect(DATABASE_URI)
            self.cursor = self.conn.cursor()
        else:
            raise ValueError("Unsupported database type. Use 'mysql' or 'postgresql'.")

    def add_data(self, network_info):
        """
        Adds network data to the database.
        :param network_info: A dictionary containing network details
        :return: None
        """
        try:
            if self.db_type == "mysql":
                query = "INSERT INTO network_configurations (network_name, bandwidth, status) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (network_info["network_name"], network_info.get("bandwidth", ""), network_info.get("status", "active")))
                self.conn.commit()
            elif self.db_type == "postgresql":
                self.cursor.execute("""
                    INSERT INTO network_data (network_name, network_ip, network_details)
                    VALUES (%s, %s, %s)
                """, (network_info["network_name"], network_info["network_ip"], network_info["network_details"]))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error adding data: {e}")
            raise e

    def retrieve_data(self, network_name):
        """
        Retrieves network data from the database.
        :param network_name: The name of the network to retrieve
        :return: Dictionary containing network data or an empty dictionary if not found
        """
        try:
            if self.db_type == "mysql":
                query = "SELECT * FROM network_configurations WHERE network_name = %s"
                self.cursor.execute(query, (network_name,))
                result = self.cursor.fetchone()
                return result if result else {}
            elif self.db_type == "postgresql":
                self.cursor.execute("SELECT * FROM network_data WHERE network_name = %s", (network_name,))
                result = self.cursor.fetchone()
                return result if result else {}
        except Exception as e:
            logging.error(f"Error retrieving data: {e}")
            return {}

    def update_data(self, network_name, status):
        """
        Updates network status in the database.
        :param network_name: The name of the network
        :param status: The new status to update
        :return: None
        """
        try:
            if self.db_type == "mysql":
                query = "UPDATE network_configurations SET status = %s WHERE network_name = %s"
                self.cursor.execute(query, (status, network_name))
                self.conn.commit()
            elif self.db_type == "postgresql":
                self.cursor.execute("UPDATE network_data SET network_status = %s WHERE network_name = %s", (status, network_name))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error updating data: {e}")
            raise e

    def close(self):
        """
        Closes the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class CleanupOperations:
    def __init__(self, log_directory="/var/log/myapp/", archive_directory="/var/log/archive/"):
        self.log_directory = log_directory
        self.archive_directory = archive_directory

    def perform_cleanup(self):
        """Archive old logs and clean up temporary files."""
        logging.info("Performing cleanup operations...")
        try:
            # Create archive directory if it doesn't exist
            if not os.path.exists(self.archive_directory):
                os.makedirs(self.archive_directory)

            # Get the current date and calculate the threshold date (e.g., 30 days old)
            threshold_date = datetime.now() - timedelta(days=30)

            # Loop through log files and archive files older than 30 days
            for filename in os.listdir(self.log_directory):
                log_file = os.path.join(self.log_directory, filename)

                # Check if the file is older than the threshold date
                if os.path.isfile(log_file):
                    file_mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                    if file_mod_time < threshold_date:
                        # Move the file to the archive folder
                        shutil.move(log_file, os.path.join(self.archive_directory, filename))
                        logging.info(f"Archived log file: {filename}")

            logging.info("Cleanup operations completed successfully.")
        
        except Exception as e:
            logging.error(f"Error during cleanup operations: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example of adding network data to the database
    network_info_mysql = {
        "network_name": "Network1",
        "bandwidth": "1Gbps",
        "status": "active"
    }
    network_info_postgresql = {
        "network_name": "Network2",
        "network_ip": "192.168.1.1",
        "network_details": "Sample network data"
    }

    # Example of using MySQL
    network_db_mysql = NetworkDatabase(db_type="mysql", host="localhost", user="root", password="password", database="vajra_network")
    try:
        network_db_mysql.add_data(network_info_mysql)
        logging.info("Network data added successfully to MySQL.")
    except Exception as e:
        logging.error(f"Error adding network data to MySQL: {e}")
    finally:
        network_db_mysql.close()

    # Example of using PostgreSQL
    network_db_postgresql = NetworkDatabase(db_type="postgresql")
    try:
        network_db_postgresql.add_data(network_info_postgresql)
        logging.info("Network data added successfully to PostgreSQL.")
    except Exception as e:
        logging.error(f"Error adding network data to PostgreSQL: {e}")
    finally:
        network_db_postgresql.close()

    # Example of performing cleanup operations
    cleanup = CleanupOperations()
    cleanup.perform_cleanup()
