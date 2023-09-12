from locust import HttpUser, task   

class Demo(HttpUser):      
    @task     
    def check_health(self):         
        self.client.get("/v1/health")  
