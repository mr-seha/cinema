FROM python:3.11-alpine3.21
RUN apk add gcc musl-dev linux-headers python3-dev
RUN apk add libffi-dev
RUN python -m pip install --upgrade pip
RUN python -m venv /venv
COPY ./requirements.txt /tmp/requirements.txt
RUN /venv/bin/pip3 install -r /tmp/requirements.txt
ENV PATH="/venv/bin:$PATH"
RUN rm -f /tmp/requirements.txt
WORKDIR /cinema
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8000", "cinema.wsgi"]
