from abc import ABC, abstractmethod

class NotifierBase(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass
