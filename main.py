from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from core.utils import filter_taks_by_name
from api_clickup import Client
from cache import Cache


class UClickUpTasksExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.api_clickup_client = Client()


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

        tasks = extension.api_clickup_client.get_tasks(token, team_id)
        task_name = event.get_argument() or ""
        tasks = filter_taks_by_name(tasks, task_name)

        print(task_name)

        for task in tasks:

            status = task["status"]["status"] if task["status"] else "No status"
            project = task["project"]["name"] if task["project"] else "No project"
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=task["name"],
                    description=str(f"{project} || {status}"),
                    on_enter=OpenUrlAction(task["url"]),
                )
            )

        return RenderResultListAction(items)


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        Cache.clean()


if __name__ == "__main__":
    UClickUpTasksExtension().run()
