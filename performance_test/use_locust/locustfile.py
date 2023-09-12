from locust import User, task

class DummyUser(User):
    @task
    def dummy_task(self):
        pass
