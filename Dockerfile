FROM python:3.11-alpine3.21

ARG DEV=true

RUN apk add gcc musl-dev linux-headers python3-dev
RUN apk add libffi-dev

RUN python -m pip install --upgrade pip
RUN python -m venv /venv

COPY ./requirements.txt ./requirements.dev.txt /tmp/
RUN /venv/bin/pip3 install -r /tmp/requirements.txt

RUN if [ $DEV == true ]; then \
    /venv/bin/pip3 install -r /tmp/requirements.dev.txt ; \
    fi


ENV PATH="/venv/bin:$PATH"

RUN rm -rf /tmp

WORKDIR /cinema
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8000", "cinema.wsgi"]
