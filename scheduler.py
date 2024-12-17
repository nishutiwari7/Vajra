import os
import shutil
import logging
import psycopg2
import schedule
import time
from datetime import datetime, timedelta
from config import DATABASE_URI


# Setting up logging for the scheduler
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class NetworkDatabase:
    def __init__(self):
        """Initialize PostgreSQL connection."""
        self.conn = psycopg2.connect(DATABASE_URI)
        self.cursor = self.conn.cursor()

    def add_data(self, network_info):
        """
        Adds network data to the database.
        :param network_info: A dictionary containing network details
        :return: None
        """
        try:
            self.cursor.execute("""
                INSERT INTO network_data (network_name, network_ip, network_details)
                VALUES (%s, %s, %s)
            """, (network_info["network_name"], network_info["network_ip"], network_info["network_details"]))
            self.conn.commit()
            logging.info(f"Network data added for {network_info['network_name']}")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error adding network data: {e}")


class CleanupOperations:
    def __init__(self, log_directory="/var/log/myapp/", archive_directory="/var/log/archive/"):
        """Initialize cleanup operations."""
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


def add_network_data_task():
    """Task to add network data."""
    # Sample network information to insert into the database
    network_info = {
        "network_name": "Network1",
        "network_ip": "192.168.1.1",
        "network_details": "Sample network data"
    }

    # Initialize NetworkDatabase instance and insert data
    network_db = NetworkDatabase()
    network_db.add_data(network_info)


def cleanup_task():
    """Task to perform cleanup operations."""
    # Initialize CleanupOperations instance and perform cleanup
    cleanup = CleanupOperations()
    cleanup.perform_cleanup()


def schedule_tasks():
    """Function to schedule the tasks."""
    # Schedule the network data insertion every 15 minutes
    schedule.every(15).minutes.do(add_network_data_task)

    # Schedule the cleanup operation every day at midnight
    schedule.every().day.at("00:00").do(cleanup_task)

    logging.info("Scheduler started. Tasks are being scheduled...")

    # Continuously run the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to prevent busy-waiting


if __name__ == "__main__":
    # Start the task scheduler
    schedule_tasks()
