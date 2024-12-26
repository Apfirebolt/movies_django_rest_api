![Django](https://img.shields.io/badge/Django-3.x-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Postgres](https://img.shields.io/badge/Postgres-12.x-blue)
![Django Rest Framework](https://img.shields.io/badge/DRF-3.x-red)

# Django Movie API

This project is a Django-based web application that provides a RESTful API for managing a collection of movies. It uses Django Rest Framework to handle API requests and responses.

For the time being this project is available at http://softgenie.org/api/movies but might be taken down in the future.

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

## Deployment

Install guvicorn server on your server

```
pip install guvicorn
```

```
gunicorn django_movie_api.wsgi:application 
```

To run the Gunicorn application in the background using `nohup`, use the following command:

Bash 

```
nohup gunicorn django_movie_api.wsgi:application &
```

Deployment through a service is in progress and would be added in near future. Also working on SSL implementation on the server.

To kill the application running through nohup use grep, search the process ID of the running application and kill it.

```
ps aux | grep "gunicorn django_movie_api.wsgi:application" | grep -v grep 

kill PID
```

- Access the API at `http://127.0.0.1:8000/api/movies/`
- Use the Django admin interface at `http://127.0.0.1:8000/admin/` to manage movies

## API Endpoints

- `GET /api/movies/` - List all movies
- `POST /api/movies/` - Create a new movie
- `GET /api/movies/{id}/` - Retrieve a specific movie
- `PUT /api/movies/{id}/` - Update a specific movie
- `DELETE /api/movies/{id}/` - Delete a specific movie

## Adding SSL

Install certbot and Nginx

```
sudo apt install python3-certbot-nginx
```

Generate certbot certificate by specifying your domain name.

```
sudo certbot --nginx -d softgenie.org -d www.softgenie.org
```

The message which you should get after successful generation of certificate

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/softgenie.org/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/softgenie.org/privkey.pem
This certificate expires on 2025-03-26.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Successfully deployed certificate for softgenie.org to /etc/nginx/sites-enabled/default
Successfully deployed certificate for www.softgenie.org to /etc/nginx/sites-enabled/default
Congratulations! You have successfully enabled HTTPS on https://softgenie.org and https://www.softgenie.org
```

Next step is to make changes in the Nginx config file which should be inside. Create a new Nginx server block.

```
sudo nano /etc/nginx/sites-available/softgenie.org
```

```
server {
    listen 80;
    server_name softgenie.org www.softgenie.org;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name softgenie.org www.softgenie.org;

    ssl_certificate /etc/letsencrypt/live/softgenie.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/softgenie.org/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

Create a symlink to enable the server block

```
sudo ln -s /etc/nginx/sites-available/sofgenie.org.com /etc/nginx/sites-enabled/
```

Test the nginx conf file with this command.

```
sudo nginx -t
```

Got the following log messages 

```
2024/12/26 11:16:59 [warn] 22878#22878: conflicting server name "softgenie.org" on 0.0.0.0:80, ignored
2024/12/26 11:16:59 [warn] 22878#22878: conflicting server name "www.softgenie.org" on 0.0.0.0:80, ignored
2024/12/26 11:16:59 [warn] 22878#22878: conflicting server name "softgenie.org" on 0.0.0.0:443, ignored
2024/12/26 11:16:59 [warn] 22878#22878: conflicting server name "www.softgenie.org" on 0.0.0.0:443, ignored
```

Restart Nginx and confirm the status

```
sudo systemctl restart nginx
sudo systemctl status nginx
```

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
