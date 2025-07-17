# CSV Operations

### Getting Started

#### Prerequisites
- Docker
- Docker Compose (usually comes with Docker Desktop)

First, install and set up Docker from [https://docs.docker.com/desktop/install/mac-install/]

```
# clone and cd into the dir
docker compose build

# migrate
docker compose run --rm backend python manage.py makemigrations

docker compose run --rm backend python manage.py migrate

docker compose run --rm backend python manage.py collectstatic --no-input

docker compose up -d

# create admin user to login to /admin/
docker compose run --rm backend python manage.py createsuperuser
```

then visit admin site at [http://localhost:8000/admin](http://localhost:8000/admin)

### Swagger APIs

You can see APIs doc at [http://localhost:8000/schema/swagger-ui/](http://localhost:8000/schema/swagger-ui/)

### Support

Contact email: tphat12a@gmail.com

