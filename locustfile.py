from faker import Faker
from locust import HttpUser, between, task


class UserFlow(HttpUser):
    fake = Faker()
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_data = {}
        self.token = ""
        self.todo_id = ""

    def on_start(self):
        self.user_data = {
            "name": f"{self.fake.name()}",
            "email": f"{self.fake.email()}",
            "password1": "test",
            "password2": "test",
        }
        self.client.post("/api/v1/user", json=self.user_data)
        response = self.client.post(
            "/api/v1/login", data={"username": self.user_data["email"], "password": self.user_data["password1"]}
        )
        self.token = {"Authorization": f"Bearer {response.json()['access_token']}"}

        self.todo_id = (
            self.client.post(
                "/api/v1/todo", json={"title": self.fake.name(), "description": self.fake.text()}, headers=self.token
            )
            .content.decode("utf-8")
            .replace('"', "")
        )

    def on_stop(self):
        pass
        # self.client.post("/api/v1/logout", headers=self.token)

    @task
    def get_todo_item(self):
        self.client.get(f"/api/v1/todo/{self.todo_id}", headers=self.token)

    @task
    def update_todo_item(self):
        self.client.put(
            f"/api/v1/todo/{self.todo_id}",
            json={"title": self.fake.name(), "description": self.fake.text()},
            headers=self.token,
        )

    @task
    def patch_todo_item(self):
        self.client.patch(f"/api/v1/todo/{self.todo_id}", params={"status": "done"}, headers=self.token)
