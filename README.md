
## VAJRA

### Overview

The **VAJRA** is an advanced simulation tool that manages BGP (Border Gateway Protocol) operations and optimizes network management for Internet Exchange Points (IXPs). It integrates with Razorpay for payment processing and provides a web-based UI for monitoring and interacting with the simulator.

This project includes:
- **BGP Simulator**: Simulates the network operations.
- **Network Database**: Manages network data and configurations.
- **Razorpay Billing**: Integrates Razorpay for billing and payments.
- **Web UI**: A Flask web app for interacting with the BGP simulator and Razorpay.

### Prerequisites

To run this project locally or in a cloud environment, ensure the following tools are installed:

-**Flask**
- **MySQL / PostgreSQL**
- **Docker** and **Docker Compose**: For containerizing and managing services.
- **Python 3.x**: For backend development
- **Razorpay Account**: For integrating the Razorpay API for payments.

#### Install Docker and Docker Compose

Follow the installation instructions for Docker and Docker Compose from the official documentation:
- [Docker Install](https://docs.docker.com/get-docker/)
- [Docker Compose Install](https://docs.docker.com/compose/install/)

### Project Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/minerva_bgp_simulator.git
cd minerva_bgp_simulator
```

#### Step 2: Set Up Razorpay Integration

Before proceeding, ensure you have Razorpay API keys. If you don't have them, create an account on [Razorpay](https://razorpay.com/). 

Update the Razorpay credentials in `razorpay_integration/config.py`:

```python
# razorpay_integration/config.py
RAZORPAY_API_KEY = "your_razorpay_api_key"
RAZORPAY_SECRET_KEY = "your_razorpay_secret_key"
```

Replace the placeholders `your_razorpay_api_key` and `your_razorpay_secret_key` with your actual Razorpay credentials.

#### Step 3: Set Up the Docker Environment

Ensure all dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This ensures that all required Python dependencies are installed.

#### Step 4: Configure Docker Compose

The `docker-compose.yaml` file is pre-configured to run the web service, Razorpay billing integration, and database services. If necessary, modify configurations such as ports, environment variables, or the database setup.

Make sure Docker is installed and running on your system. If you're unsure, check by running:

```bash
docker --version
docker-compose --version
```

#### Step 5: Running the Application with Docker Compose

Run the following command to build and start the containers:

```bash
docker-compose up --build
```

This will:
- Build the Docker images for your services.
- Start the containers for the web service (`Flask` app), Razorpay integration, and database.

The application will be accessible at `http://localhost:5000/`.

#### Step 6: Accessing the Web Interface

Once the application is running, navigate to `http://localhost:5000/` in your browser. You will see the main interface where you can interact with the BGP simulator, view the network database, and process payments through Razorpay.

- **Razorpay Payment Links**:
  - [INR Payment Link](https://rzp.io/rzp/JusDG4P)
  - [USD Payment Link](https://rzp.io/rzp/BblrH9g9)

#### Step 7: Testing the Application

Unit tests for various components (BGP Simulator, Network Database, and Razorpay Integration) are available in the `tests/` directory. To run the tests, use:

```bash
pytest tests/
```

This will automatically detect and run all test files (e.g., `test_bgp_simulator.py`, `test_network_database.py`, `test_billing_system.py`, etc.).

#### Step 8: Making Changes to the Code

If you need to modify or extend the functionality, follow these steps:

1. **Modify the Backend (Python)**:
   - The primary logic for BGP simulation is located in `bgp_simulator.py`.
   - You can update network configurations, routing policies, or simulation parameters as needed.
   - Billing integration is handled by `billing_system.py` in the `razorpay_integration/` directory. Modify this for custom billing logic.
   
2. **Modify the Frontend (UI)**:
   - The web UI is built with Flask and uses the `templates/index.html` for rendering. You can update this template to change the interface, add new features, or modify existing pages.
   - The `static/style.css` file is where you can change the look and feel of the application. Add your own CSS styles if needed.

3. **Database Changes**:
   - If you need to change the database setup (for example, using MySQL instead of SQLite), you can modify the `docker-compose.yaml` to include a different database service, and adjust the code accordingly.

4. **Scheduler**:
   - The scheduler (`scheduler.py`) can be used for periodic tasks such as updating network configurations, billing, or cleanup operations.

### Step 9: Deploying to AWS

To deploy this project to AWS using Docker, follow these steps:

1. **Set up an EC2 Instance**:
   - Create an EC2 instance using the AWS console and install Docker on the instance.

2. **Copy the Code to EC2**:
   - Use `scp` or any file transfer method to copy the project files to your EC2 instance.

3. **Run Docker on EC2**:
   - SSH into the EC2 instance and navigate to the project directory.
   - Run `docker-compose up --build` to start the containers.

4. **Configure AWS Networking**:
   - Ensure that your EC2 instance has a public IP and security group settings to allow HTTP traffic (port 5000).
   - Access the application via `http://<EC2_PUBLIC_IP>:5000`.

### Step 10: Stopping the Services

To stop the containers, use the following command:

```bash
docker-compose down
```

This will stop and remove all containers, but the data will remain in your local volumes.

---

## Swarm Mode Consideration:

To enable scaling in Swarm mode, you'll need to initialize Docker Swarm on your machine or server. You can do this by running:

```bash
docker swarm init
```

Then deploy your services using:

```bash
docker stack deploy -c docker-compose.yml vajra
```

---

## Running in Docker Swarm Mode:

1. **Initialize Docker Swarm**:
   If not already initialized, run:

   ```bash
   docker swarm init
   ```

2. **Deploy the Stack**:
   Use the following command to deploy the stack with the scaled web service:

   ```bash
   docker stack deploy -c docker-compose.yml vajra
   ```

3. **Scaling the Web Service**:
   You can adjust the number of replicas dynamically with Docker Swarm using:

   ```bash
   docker service scale vajra_web=3
   ```

This setup will efficiently scale the Flask web service (`vajra_web`) to 3 instances and ensure that all services are properly orchestrated in Docker Swarm mode.

---

## Project Structure

```
VAJRA/
│
├── sql_files/
│   ├── create_database.sql         # Contains the schema definition
│   ├── insert_data.sql            # Contains sample data
│   └── update_data.sql            # Contains data update scripts
│
├── main.py                        # Entry point for running the application
├── scheduler.py                   # Main application logic
├── bgp_simulator.py               # BGP simulation code
├── network_database.py            # Network Database management
├── billing_system.py              # Razorpay Billing Integration with Database
├── optimizer.py                   # Network optimization logic
├── azure_peering.py               # Azure VNet peering automation
├── ixp_manager.py                 # Manages IXP access before others
├── ui_service/
│   ├── app.py                     # Flask app for IXP and Razorpay UI
│   ├── templates/
│   │   └── index.html             # Unified UI for IXP and billing management
│   └── static/
│       ├── style.css
│       └── main.js                # JavaScript for UI interactivity
├── config.py                      # Razorpay and project configurations
├── tests/
│   ├── test_bgp_simulator.py      # Unit tests for BGP simulation
│   ├── test_network_database.py   # Unit tests for network database
│   ├── test_billing_system.py     # Unit tests for Razorpay billing
│   ├── test_ixp_manager.py        # Unit tests for IXP access management
│   └── test_ui_service.py         # Unit tests for Flask Razorpay integration
├── requirements.txt               # Combined dependencies for the project
├── docker-compose.yaml            # Docker setup for easy deployment
└── README.md                      # Project documentation and instructions


```
## MIT License

Copyright (c) 2024 [VAJRA]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

## Conclusion

With this setup, you can easily simulate and optimize BGP operations, manage network data, and integrate payments via Razorpay. Docker ensures easy deployment and scalability, making it suitable for both local and cloud environments.

If you have any questions or need further help, feel free to open an issue or contact the maintainers.

---