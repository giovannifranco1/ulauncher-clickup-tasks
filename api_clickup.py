import requests
from cache import Cache


class Client(object):
    """
    Class to interact with ClickUp API
    """

    API_URL = "https://api.clickup.com/api/v2"

    CACHE_KEY = "tasks"

    CACHE_TTL = 60

    def get_tasks(self, token, team_id):
        """
        Get tasks from ClickUp API
        """

        if Cache.get(self.CACHE_KEY):
            return Cache.get(self.CACHE_KEY)

        response = requests.get(f"{self.API_URL}/team/{team_id}/task", headers={"Authorization": token})

        if not response.ok:
            response.raise_for_status()

        data = response.json()
        tasks = data.get("tasks", [])
        Cache.set(self.CACHE_KEY, tasks, self.CACHE_TTL)

        return tasks
