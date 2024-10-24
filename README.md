# DjangoAuthbridge: Django Microservices with Keycloak and Kerberos Authentication

This project is a microservices architecture built using Django and Docker, integrated with Keycloak for centralized authentication (SSO) and Kerberos for network authentication. The microservices communicate with their respective PostgreSQL databases, and NGINX is used as a reverse proxy.

## Project Structure

```
├── config/
│   ├── kerberos/              # Kerberos KDC configuration and files
│   ├── keycloak/              # Keycloak authentication service configuration
│   ├── keytabs/               # Kerberos keytab files for services
│   ├── nginx/                 # NGINX reverse proxy configuration
│   ├── postgres_data/         # PostgreSQL database volumes
│   └── docker-compose.yml     # Docker Compose file to orchestrate the setup
├── microservice1/             # Django microservice 1
│   ├── base/                  # Django app files
│   ├── Dockerfile             # Dockerfile to build microservice1
│   └── requirements.txt       # Python dependencies for microservice1
├── microservice2/             # Django microservice 2
│   ├── base/                  # Django app files
│   ├── Dockerfile             # Dockerfile to build microservice2
│   └── requirements.txt       # Python dependencies for microservice2
├── microservice3/             # Django microservice 3
│   ├── base/                  # Django app files
│   ├── Dockerfile             # Dockerfile to build microservice3
│   └── requirements.txt       # Python dependencies for microservice3
├── venv/                      # Python virtual environment (local development, ignored by Git)
├── .gitignore                 # Specifies files and directories to ignore in Git
├── .gitattributes             # Defines file attribute settings for Git
├── LICENSE                    # License for the project
└── README.md                  # Project documentation (this file)
```

## Services Overview

### 1. **Keycloak** - Centralized Authentication (SSO)
- **Keycloak** is an open-source identity and access management tool used for authentication and authorization. It manages user login for all microservices.
- **Keycloak Database** (`keycloak_db`): A PostgreSQL instance that stores Keycloak data.

### 2. **Django Microservices**
Each microservice is a separate Django application with its own PostgreSQL database.

- **Microservice 1**: 
  - Runs on port `8001`.
  - Connects to PostgreSQL database `microservice1_db`.

- **Microservice 2**:
  - Runs on port `8002`.
  - Connects to PostgreSQL database `microservice2_db`.

- **Microservice 3**:
  - Runs on port `8003`.
  - Connects to PostgreSQL database `microservice3_db`.

### 3. **PostgreSQL Databases**
- Each microservice has its own dedicated PostgreSQL database.
  - `microservice1_db`: For Microservice 1.
  - `microservice2_db`: For Microservice 2.
  - `microservice3_db`: For Microservice 3.

### 4. **NGINX Reverse Proxy**
- NGINX is used to reverse proxy and route requests to the correct microservice based on the incoming URL.

### 5. **Kerberos KDC (Key Distribution Center)**
- **Kerberos** is used for network authentication, ensuring secure communication and enabling Single Sign-On (SSO) across the system.
- The **Kerberos KDC** service runs as a container and manages authentication tickets for services.

## Docker Compose Setup

### Docker Services

The `docker-compose.yml` file orchestrates the following services:
- **Keycloak** (`keycloak_con`) and **Keycloak DB** (`keycloak_db`): Manages user authentication.
- **Microservice 1** (`microservice1_con`): Django microservice with its own database.
- **Microservice 2** (`microservice2_con`): Django microservice with its own database.
- **Microservice 3** (`microservice3_con`): Django microservice with its own database.
- **Kerberos KDC** (`kerberos_kdc`): Kerberos authentication service.
- **PostgreSQL** for each microservice.

### Running the Services

To start all the services, run the following command from the root directory:

```bash
docker-compose up --build
```

This command will build and start all containers defined in `docker-compose.yml`.

### Accessing the Services

- **Keycloak**: [http://localhost:8080](http://localhost:8080) - Centralized authentication UI.
- **Microservice 1**: [http://localhost:8001](http://localhost:8001) - Django service for microservice1.
- **Microservice 2**: [http://localhost:8002](http://localhost:8002) - Django service for microservice2.
- **Microservice 3**: [http://localhost:8003](http://localhost:8003) - Django service for microservice3.

## Environment Variables

Environment variables for each service are defined in the `docker-compose.yml` file:

- **Keycloak**:
  - `KEYCLOAK_USER`: The admin user for Keycloak.
  - `KEYCLOAK_PASSWORD`: The admin password for Keycloak.
  - `DB_VENDOR`: Database vendor (PostgreSQL).
  - `DB_ADDR`, `DB_DATABASE`, `DB_USER`, `DB_PASSWORD`: PostgreSQL connection details.

- **Microservices**:
  - `DB_HOST`, `DB_PORT`: PostgreSQL host and port.
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL database connection details.

- **Kerberos**:
  - `REALM`: Kerberos realm name.
  - `KDC_DOMAIN`: Kerberos domain.
  - `KRB5_KEYTAB`: Path to the Kerberos keytab file.

## Persisting Data

- PostgreSQL data is stored in the `config/postgres_data/` directory, ensuring that data persists even if the containers are stopped or removed.

## SSO Integration with Keycloak

To enable Single Sign-On (SSO) with Keycloak, follow these steps:

### 1. Keycloak Setup
- **Install and Configure Keycloak**:
  - Deploy Keycloak using Docker (as per your existing setup in the `docker-compose.yml`).
  - Access the Keycloak admin console at `http://localhost:8080/auth` and log in using the admin credentials.

- **Create a Realm**:
  - In the Keycloak Admin Console, click **Add Realm**, name it (e.g., `myrealm`), and save.

- **Create Clients for Each Microservice**:
  - In Keycloak, go to the **Clients** tab and click **Create** for each microservice (e.g., `microservice1`, `microservice2`, `microservice3`).
  - Set **Client Protocol** to `openid-connect` and **Access Type** to `confidential`.
  - Save the client and copy the **Client Secret** (you will need this in Django settings).

- **Create Users**:
  - Go to the **Users** section, click **Add User**, and create a user for each service.

### 2. Integrating Keycloak with Django Microservices
- Install the necessary Python package for Keycloak integration:
  ```bash
  pip install django-keycloak-auth
  ```

- Update the Django settings for each microservice (`settings.py`):
  - Add Keycloak configurations such as:
    ```python
    KEYCLOAK_CONFIG = {
        'KEYCLOAK_SERVER_URL': 'http://localhost:8080/auth',
        'KEYCLOAK_CLIENT_ID': 'microservice1',
        'KEYCLOAK_REALM': 'myrealm',
        'KEYCLOAK_CLIENT_SECRET': 'your-client-secret-here',
        'KEYCLOAK_OPENID_CONFIG': '/realms/myrealm/.well-known/openid-configuration',
    }
    ```

### 3. Testing the SSO Integration
- Start all services using `docker-compose up`.
- Visit each microservice URL, and you will be redirected to Keycloak for authentication.

## Troubleshooting

If you encounter any issues, you can check the logs of the individual services:

```bash
docker-compose logs <service_name>
```

For example, to check the logs of microservice1:

```bash
docker-compose logs microservice1
```

## Future Improvements

- Implement scaling strategies for microservices and databases.
- Add monitoring and logging tools (such as Prometheus, Grafana, or ELK stack).
- Enhance security configurations for production environments.


## Contributors

| [<img src="https://github.com/Mritunjaypratapsinghh.png?size=100" width="100px;"/><br /><sub><b>Mritunjay Pratap Singh</b></sub>](https://github.com/Mritunjaypratapsinghh) | [<img src="https://github.com/Mohdsakib535.png?size=100" width="100px;"/><br /><sub><b>Mohd Sakib</b></sub>](https://github.com/Mohdsakib535) |
| :---: | :---: |


