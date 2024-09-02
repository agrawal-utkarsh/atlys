from .notifier import NotifierBase

class ConsoleNotifier(NotifierBase):
    def notify(self, message: str):
        print(message)
