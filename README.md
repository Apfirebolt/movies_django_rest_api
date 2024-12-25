![Django](https://img.shields.io/badge/Django-3.x-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Postgres](https://img.shields.io/badge/Postgres-12.x-blue)
![Django Rest Framework](https://img.shields.io/badge/DRF-3.x-red)

# Django Movie API

This project is a Django-based web application that provides a RESTful API for managing a collection of movies. It uses Django Rest Framework to handle API requests and responses.

## Features

- Add, update, delete, and retrieve movies
- Search for movies by title or genre
- Pagination for large datasets
- Authentication and authorization

## Requirements

- Python 3.12
- Django 5.1.4
- Django Rest Framework
- Postgresql

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/django_movie_api.git
    cd django_movie_api
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

- Access the API at `http://127.0.0.1:8000/api/movies/`
- Use the Django admin interface at `http://127.0.0.1:8000/admin/` to manage movies

## API Endpoints

- `GET /api/movies/` - List all movies
- `POST /api/movies/` - Create a new movie
- `GET /api/movies/{id}/` - Retrieve a specific movie
- `PUT /api/movies/{id}/` - Update a specific movie
- `DELETE /api/movies/{id}/` - Delete a specific movie

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
