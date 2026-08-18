# Django Movie API Deployment Summary & Runbook

This document summarizes the changes, fixes, and current deployment configuration for running the **Django Movie REST API** with **Supervisor**, **Gunicorn**, and **Nginx** (with SSL / Let's Encrypt).

---

## 1. Problem Identification & Root Cause

| Issue Observed | Root Cause | Resolution |
| :--- | :--- | :--- |
| `unix:///tmp/supervisor.sock no such file` | The Supervisor daemon (`supervisord`) was either not running or using system paths (`/var/run/supervisor.sock`), while client commands pointed to `/tmp/`. Additionally, OS reboots wipe `/tmp/`. | Switched to a project-contained, persistent socket path (`/home/movies_django_rest_api/supervisor.sock`) and disabled conflicting system daemons. |
| Application stopped after server reboot | Supervisor had been started manually without an active boot mechanism or was conflicting with disabled unit scripts. | Disabled the redundant system-wide unit and configured a persistent boot strategy (`crontab` / `@reboot`). |
| Port 8000 exposed externally (`0.0.0.0`) | Gunicorn was directly reachable from the public network, bypassing Nginx security, rate limits, and caching. | Re-bound Gunicorn strictly to `127.0.0.1:8000` (loopback). |
| Missing static file handling in Nginx | Static assets were passing through Python Gunicorn workers rather than being served directly. | Added optimized `/static/` and `/media/` location blocks with long caching headers. |

---

## 2. Configuration Files Reference

### A. Supervisor Configuration
**File path:** `/home/movies_django_rest_api/supervisord.conf`

```ini
[unix_http_server]
file=/home/movies_django_rest_api/supervisor.sock
chmod=0700

[supervisord]
logfile=/home/movies_django_rest_api/logs/supervisord.log
logfile_maxbytes=50MB
logfile_backups=5
loglevel=info
pidfile=/home/movies_django_rest_api/supervisord.pid
nodaemon=false
minfds=1024
minprocs=200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///home/movies_django_rest_api/supervisor.sock

[program:django_movie_api]
command=/home/movies_django_rest_api/venv/bin/gunicorn django_movie_api.wsgi:application --workers 3 --bind 127.0.0.1:8000
directory=/home/movies_django_rest_api
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=60
stopsignal=TERM
stopasgroup=true
killasgroup=true

# Logging & Rotation
stdout_logfile=/home/movies_django_rest_api/logs/django_movie_api.out.log
stdout_logfile_maxbytes=20MB
stdout_logfile_backups=5
stderr_logfile=/home/movies_django_rest_api/logs/django_movie_api.err.log
stderr_logfile_maxbytes=20MB
stderr_logfile_backups=5

# Environment
environment=DJANGO_SETTINGS_MODULE="django_movie_api.settings"
```

---

### B. Nginx Server Block
**File path:** `/etc/nginx/sites-available/default` (or `/etc/nginx/conf.d/default.conf`)

```nginx
# 1. HTTP: Redirect all plain HTTP traffic to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name softgenie.org www.softgenie.org;

    return 301 https://$host$request_uri;
}

# 2. HTTPS: SSL Termination & Gunicorn Reverse Proxy
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name softgenie.org www.softgenie.org;

    # SSL Certificates (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/softgenie.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/softgenie.org/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Maximum upload limit
    client_max_body_size 20M;

    # Django Static Files
    location /static/ {
        alias /home/movies_django_rest_api/staticfiles/;
        expires 30d;
        access_log off;
    }

    # Django Media Uploads
    location /media/ {
        alias /home/movies_django_rest_api/media/;
        expires 30d;
        access_log off;
    }

    # Reverse Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 3. Server Architecture Overview

```
 [Client Browser / API Consumer]
                 │ (Port 80 / 443)
                 ▼
         [Nginx Web Server]
          ├── /static/  ──────► Filesystem (/staticfiles/)
          ├── /media/   ──────► Filesystem (/media/)
          └── / (Proxy) ──────► 127.0.0.1:8000
                                       │
                                       ▼
                       [Gunicorn WSGI (3 Workers)]
                                       │
                                       ▼
                     [Supervisor Process Manager]
                   (Socket: supervisor.sock / PID: supervisord.pid)
```

---

## 4. Operational Runbook & Cheat Sheet

### Managing Application via Supervisor
All supervisorctl commands must specify the project configuration file path using `-c`:

```bash
# Check service status
supervisorctl -c /home/movies_django_rest_api/supervisord.conf status

# Restart the Django API (e.g. after code updates)
supervisorctl -c /home/movies_django_rest_api/supervisord.conf restart django_movie_api

# Stop / Start the application
supervisorctl -c /home/movies_django_rest_api/supervisord.conf stop django_movie_api
supervisorctl -c /home/movies_django_rest_api/supervisord.conf start django_movie_api

# Stream application logs live
supervisorctl -c /home/movies_django_rest_api/supervisord.conf tail -f django_movie_api stderr
```

---

### Managing Nginx
```bash
# Test configuration syntax
sudo nginx -t

# Reload without downtime
sudo systemctl reload nginx

# Check status
sudo systemctl status nginx
```

---

### Server Boot Persistence
Ensure that your crontab has the reboot directive enabled:
```bash
# Edit crontab
crontab -e

# Add line:
@reboot /usr/bin/supervisord -c /home/movies_django_rest_api/supervisord.conf
```