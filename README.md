# 🎬 API for a Movie Download Website

A comprehensive RESTful API for a movie download website, developed using Django & Django REST Framework.

## Overview

This project provides a robust backend system for a movie download website, offering functionalities such as:

* User Registration, login, and profile management
* Movie listing and detailed views
* Download link management
* Administrative controls for content management

## Technologies Used

* **Python**
* **Django**
* **Django REST Framework**
* **Docker & Docker Compose**
* **Celery & Redis** to manage background tasks
* **Pytest** for testing
* **Locust** for performance testing
* **Silk** for live profiling
* **Flake8** for code linting


## Getting Started

**Clone the repository:**

   ```bash
   git clone https://github.com/mr-seha/cinema.git
   cd cinema
   ```

### Run via pipenv

1. **Install pipenv:**

   ```bash
   pip install --user pipenv
   ```

2. **Activate the virtual environment:**

   ```bash
   pipenv shell
   ```
3. **Install dependencies:**

   In the same terminal, run:
   ```bash
   pipenv install --dev --skip-lock
   ```
4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run server:**

   Run the development server:
   ```bash
   python manage.py runserver
   ```

   Or run with gunicorn:
   ```bash
   gunicorn cinema.wsgi
   ```
6. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```
      
### Run via docker & docker compose

1. **Build and start the containers:**

   ```bash
   docker compose up --build
   ```
   
2. **Apply migrations:**

   In a new terminal window, run:

   ```bash
   docker compose run --rm backend python manage.py migrate
   ```

3. **Create a superuser (optional):**

   ```bash
   docker compose run --rm backend python manage.py createsuperuser
   ```
   
**Access the application:**

   * API Root: [http://localhost:8000/api/](http://localhost:8000/api/)
   * API Documentation(Swagger): [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
   * API Documentation(Redoc): [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
   * Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
   * Live profiling: [http://localhost:8000/silk/](http://localhost:8000/silk/)

## Running Tests

To execute the test suite:

```bash
docker compose run --rm backend pytest
```
Alternatively, use pytest-watch for continuous testing
```bash
docker compose run --rm backend ptw
```

## Author

Developed by **Mohammadreza Souri**

## License

This project is open for public use.  
Feel free to use, modify, and share it without restrictions.
