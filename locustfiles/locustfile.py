from random import randint

from locust import HttpUser, task, between


class WebSiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(4)
    def view_films(self):
        genre_id = randint(1, 4)
        self.client.get(f"/films/?genre_id={genre_id}/", name="/films")

    @task(9)
    def view_film(self):
        film_id = [1, 2, 6][randint(0, 2)]
        self.client.get(f"/films/{film_id}/", name="/films/id")

    @task(1)
    def view_genres(self):
        self.client.get("/genres/", name="/genres")

    @task
    def browse_film_comments(self):
        film_id = randint(1, 5)
        self.client.get(f"/films/{film_id}/comments/")
