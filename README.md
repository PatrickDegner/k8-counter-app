# Hit Counter App

This application demonstrates a simple hit counter using a Python backend with FastAPI, a MySQL database, and a Python frontend, all deployed on Kubernetes.

## Architecture

The application consists of three main components:

- **counter-backend:** A FastAPI application that increments a counter in the MySQL database and returns the current count, along with the pod's hostname and IP address.
- **counter-db:** A MySQL database to store the counter value, deployed with persistent storage.
- **counter-frontend:** A FastAPI application that displays the current counter value fetched from the backend and the backend pod's hostname.

## Setup and Deployment

1. **Database Initialization:**
   - **Port Forwarding:**
      -  Forward the port from your local machine to the `counter-db` pod:
         ```bash
         kubectl port-forward service/counter-db 3306:3306
         ```
   - **Connect to MySQL:**
      - Use your preferred MySQL client (e.g., `mysql` command-line client, MySQL Workbench) with the following details:
          - **Host:** `localhost`
          - **Port:** `3306`
          - **User:** `root`
          - **Password:** `password`
      - **Example using `mysql` client:**
         ```bash
         mysql -h localhost -u root -p
         ```
   - **Create Database and Table:**
      - Execute the following SQL commands:
        ```sql
        CREATE TABLE apicounter.counter_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            count INT DEFAULT 0
        );

        INSERT INTO counter_table(id, count) VALUES (1, 0);
        ```

2. **Build and Push Docker Images:**
   - **Build:**
      - Navigate to each component directory (`counter-backend` and `counter-frontend`) and build the Docker images, replacing `<your-dockerhub-username>` with your Docker Hub username:
         ```bash
         docker build -t <your-dockerhub-username>/counter-backend:latest .
         docker build -t <your-dockerhub-username>/counter-frontend:latest . 
         ```
   - **Push:**
      - Push the images to Docker Hub:
         ```bash
         docker push <your-dockerhub-username>/counter-backend:latest
         docker push <your-dockerhub-username>/counter-frontend:latest
         ```
   - **Update Deployment YAMLs:**
      - In `counter-backend/deployment.yaml` and `counter-frontend/deployment.yaml`, replace `patrickdeg/counter-backend:latest` and `patrickdeg/counter-frontend:latest` with your Docker Hub image URLs (e.g., `<your-dockerhub-username>/counter-backend:latest`).

3. **Kubernetes Deployment:**
   - Apply the Kubernetes YAML files in the following order:
      - `kubectl apply -f counter-db/pv-claim.yaml`
      - `kubectl apply -f counter-db/deployment.yaml`
      - `kubectl apply -f counter-db/service.yaml`
      - `kubectl apply -f counter-backend/deployment.yaml`
      - `kubectl apply -f counter-backend/service.yaml`
      - `kubectl apply -f counter-frontend/deployment.yaml`
      - `kubectl apply -f counter-frontend/service.yaml`

4. **Access the Application:**
   - Find the external IP or NodePort of the `frontend-service` using `kubectl get services`.
   - Open a web browser and navigate to the application URL (e.g., `http://<external-ip>:<nodeport>/`).

## Code Overview

### Backend (`counter-backend`)

- **`main.py`:**  
    - Uses FastAPI to create an API endpoint.
    - Connects to the MySQL database using environment variables for connection details.
    - Increments the counter in the `counter_table`.
    - Retrieves the updated counter value.
    - Returns the counter value, pod hostname, and pod IP address in JSON format.

- **`Dockerfile`:**
    - Uses Python 3.12 as the base image.
    - Sets the working directory.
    - Installs dependencies from `requirements.txt`.
    - Copies the application code.
    - Defines the command to run the Uvicorn server.

### Frontend (`counter-frontend`)

- **`main.py`:** 
    - Uses FastAPI to create a web application.
    - Uses Jinja2 templates to render HTML.
    - Fetches the counter value and backend hostname from the backend API.
    - Renders the `index.html` template with the fetched data.
    - Handles potential errors and renders the `error.html` template if necessary.

- **`Dockerfile`:**
    - Similar to the backend Dockerfile, builds a Docker image for the frontend application.

## Dependencies

- FastAPI
- Uvicorn
- Jinja2
- requests
- mysql-connector-python
