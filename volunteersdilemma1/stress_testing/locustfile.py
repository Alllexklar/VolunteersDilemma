from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        # Join the session so that cookies are set.
        with self.client.get("/join/vejikubu", catch_response=True) as join_resp:
            if join_resp.status_code != 200:
                join_resp.failure("Join failed")

    @task
    def full_flow(self):
        # GET AnimalChoice page
        with self.client.get("/dilemma1/AnimalChoice/1", catch_response=True) as animal_choice_resp:
            if animal_choice_resp.status_code != 200:
                animal_choice_resp.failure("Failed to load AnimalChoice page")
        
        # POST a pet choice to AnimalChoice.
        with self.client.post("/dilemma1/AnimalChoice/1", data={"pet_choice": "dog"}, catch_response=True) as post_resp:
            if post_resp.status_code not in (200, 302):
                post_resp.failure("Failed to submit pet choice")
        
        # GET MywaitingPage.
        with self.client.get("/dilemma1/MywaitingPage/2", catch_response=True) as waiting_resp:
            if waiting_resp.status_code != 200:
                waiting_resp.failure("Failed to load MywaitingPage")
