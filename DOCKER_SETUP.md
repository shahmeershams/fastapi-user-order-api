# Docker Setup

Hey! So the docker-compose.yml file isn't in this project anymore. Here's how to set it up:

## Quick Setup

First, make a docker folder outside this project:
```bash
mkdir ../docker
cd ../docker
```

Then create a `docker-compose.yml` file there with this content:
```yaml
version: "3.9"
services:
  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: secret123
      MYSQL_DATABASE: orders_db
      MYSQL_USER: admin
      MYSQL_PASSWORD: secret123
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## Running Everything

Start the database:
```bash
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
