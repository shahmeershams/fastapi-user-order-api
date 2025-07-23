# Docker Setup

Hey! So the docker-compose.yml file isn't in this project anymore. Here's how to set it up:

## Quick Setup

The docker-compose.yml file is now in a shared docker folder outside this project:
```bash
cd ../docker
```

The docker-compose.yml file is already there with this content:
```yaml
version: "3.9"
services:
  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## Environment Variables
Create a `.env` file in the docker folder with your actual values:
```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=orders_db
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
```

## Running Everything

Start the database:
```bash
cd ../docker
docker-compose up -d
```

Then go back to the project and run the app:
```bash
cd ../fastapi-user-order-api
uvicorn main:app --reload
```

That's it! The app will connect to the database automatically using the settings in the `.env` file.

## Stopping

When you're done:
```bash
cd ../docker
docker-compose down
```
