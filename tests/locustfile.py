import itertools
import random

from locust import HttpUser, task, between

UID_RANGE = range(100, 1000)


class RankingUser(HttpUser):
    wait_time = between(0.5, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid_cycle = itertools.cycle(UID_RANGE)

        offset = random.randint(0, len(UID_RANGE) - 1)
        for _ in range(offset):
            next(self.uid_cycle)

    @task
    def get_recommendations(self):
        uid = next(self.uid_cycle)
        self.client.get(f'/recommendations?user_id={uid}', name='/recommendations')
