# Installation Guide

This guide provides detailed instructions for installing and running Fauxmots in different environments.

## Local Development Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/username/fauxmots.git
   cd fauxmots
   ```

   Alternatively, download and extract the ZIP file from GitHub.

2. **Set up a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python run.py
   ```

   This starts:
   - Web interface at http://127.0.0.1:5000
   - SMTP server at 127.0.0.1:1025

5. **Automated setup**

   For convenience, you can use the provided setup script:

   ```bash
   chmod +x init_dev_env.sh  # Make executable if needed
   ./init_dev_env.sh
   ```

## Docker Installation

### Prerequisites

- Docker
- Docker Compose (optional, for using docker-compose.yml)

### Using Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/username/fauxmots.git
   cd fauxmots
   ```

2. **Start the container**

   ```bash
   docker-compose up -d
   ```

   This will build the image if needed and start the container in detached mode.

3. **Access the application**

   - Web interface: http://localhost:5000
   - SMTP server: localhost:1025

4. **View logs**

   ```bash
   docker-compose logs -f
   ```

5. **Stop the container**

   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build the Docker image**

   ```bash
   docker build -t fauxmots .
   ```

2. **Run the container**

   ```bash
   docker run -d -p 5000:5000 -p 1025:1025 \
     -v $(pwd)/emails:/app/emails \
     -v $(pwd)/instance:/app/instance \
     --name fauxmots fauxmots \
     python -c 'from app.cli import main; main()' --host=0.0.0.0 --port=5000 --smtp-host=0.0.0.0 --smtp-port=1025
   ```

3. **Access the application**

   - Web interface: http://localhost:5000
   - SMTP server: localhost:1025

4. **View logs**

   ```bash
   docker logs -f fauxmots
   ```

5. **Stop and remove the container**

   ```bash
   docker stop fauxmots
   docker rm fauxmots
   ```

## Production Deployment

For production environments, consider the following recommendations:

1. **Use HTTPS**: Set up a reverse proxy like Nginx with SSL/TLS certificates.

2. **Use environment variables** for configuration instead of hardcoded values.

3. **Restrict access** to the SMTP server to only trusted networks.

4. **Regular backups** of the SQLite database in the instance directory.

5. **Monitoring and logging** to track server health and usage.

## Troubleshooting

### Common Issues

1. **Port conflicts**: If ports 5000 or 1025 are already in use, change them using the command-line options:
   ```bash
   python run.py --port 8080 --smtp-port 2525
   ```

2. **Permission errors**: Make sure the directories for emails and instance have proper write permissions.

3. **Database errors**: If you encounter database errors, try deleting the SQLite file in the instance directory and restart the application.

4. **SMTP connection issues**: Ensure your firewall allows connections to the SMTP port.

For further assistance, please open an issue on GitHub.
