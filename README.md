# 🎬 API for a Movie Download Website

A comprehensive RESTful API for a movie download website, developed using Django REST Framework.

## Overview

This project provides a robust backend system for a movie download website, offering functionalities such as:

* User authentication and authorization
* Movie listing and detailed views
* Download link management
* Administrative controls for content management

## 🛠️ Technologies Used

* **Python**
* **Django**
* **Django REST Framework**
* **Docker & Docker Compose**
* **Celery & Redis** to manage background tasks
* **pytest** for testing
* **Locust** for performance testing
* **Silk** for live profiling
* **flake8** for code linting


## Getting Started

### Prerequisites

* Docker
* Docker Compose

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mr-seha/cinema.git
   cd cinema
   ```

2. **Build and start the containers:**

   ```bash
   docker compose up --build
   ```

3. **Apply migrations:**

   In a new terminal window, run:

   ```bash
   docker compose exec backend sh -c "python manage.py migrate"
   ```

4. **Create a superuser (optional):**

   ```bash
   docker compose exec backend sh -c "python manage.py createsuperuser"
   ```

5. **Access the application:**

   * API Root: [http://localhost:8000/api/](http://localhost:8000/api/)
   * API Documentation: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
   * Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Running Tests

To execute the test suite:

```bash
docker compose exec backend sh -c pytest
```


## Author

Developed by **Mohammadreza Souri**

## License

This project is open for public use.  
Feel free to use, modify, and share it without restrictions.
