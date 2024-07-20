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
        team_id = extension.preferences.get("team_id")  # Get the value of the pk_team_id preference

        if not token:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="ClickUp token not set",
                        description="Please set your ClickUp token in the extension preferences",
                        on_enter=HideWindowAction(),
                    )
                ]
            )

        if not team_id:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="ClickUp team ID not set",
                        description="Please set your ClickUp team ID in the extension preferences",
                        on_enter=HideWindowAction(),
                    )
                ]
            )

        try:
            response = requests.get(f"https://api.clickup.com/api/v2/team/{team_id}/task", headers={"Authorization": token})
        except requests.exceptions.RequestException as e:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Error fetching tasks",
                        description=str(e),
                        on_enter=HideWindowAction(),
                    )
                ]
            )

        tasks = response.json()["tasks"]
        task_name = event.get_argument() or ""
        tasks = filter_taks_by_name(tasks, task_name)

        print(task_name)

        for task in tasks:
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=task["name"],
                    description=str(task["description"]),
                    on_enter=HideWindowAction(),
                )
            )

        return RenderResultListAction(items)


# class PreferencesEventListener(EventListener):
#     def on_event(self, event, extension):
#         extension.token = event.preferences["token"]  # Set the value of the pk_token preference
#         return HideWindowAction()


if __name__ == "__main__":
    UClickUpTasksExtension().run()
