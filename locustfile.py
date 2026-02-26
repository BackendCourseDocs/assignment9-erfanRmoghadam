from locust import HttpUser, task, between
import random

queries = ["python", "java", "design", "linux", "ai"]

class BookSearchUser(HttpUser):
    wait_time = between(1, 3)


    @task
    def search_books(self):
        q = random.choice(queries)
        self.client.get(f"/search?q={q}&page=1&size=3")