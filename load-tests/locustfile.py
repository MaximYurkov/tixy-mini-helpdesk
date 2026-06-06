from locust import HttpUser, task, between


class HelpdeskUser(HttpUser):
    wait_time = between(0.05, 0.2)

    @task(3)
    def health(self):
        self.client.get("/api/health", name="/api/health")

    @task(1)
    def graphql_hello(self):
        self.client.post(
            "/graphql",
            json={"query": "{ hello }"},
            name="/graphql hello",
        )