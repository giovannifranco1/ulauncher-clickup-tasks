from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from core.utils import filter_taks_by_name
import requests


class UClickUpTasksExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.token = None


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        token = extension.preferences.get("token")  # Get the value of the pk_token preference
        response = requests.get("https://api.clickup.com/api/v2/task/", headers={"Authorization": token})

        tasks = response.json()["tasks"]
        task_name = event.get_argument() or ""
        tasks = filter_taks_by_name(tasks, task_name)

        for task in tasks:
            items.append(
                ExtensionResultItem(icon="images/icon.png", name=task["name"], description=task["description"], on_enter=HideWindowAction())
            )

        return RenderResultListAction(items)


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.token = event.preferences["token"]  # Set the value of the pk_token preference
        return HideWindowAction()


if __name__ == "__main__":
    UClickUpTasksExtension().run()
