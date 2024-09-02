from abc import ABC, abstractmethod

class StorageBase(ABC):
    @abstractmethod
    def save(self, data: list):
        pass

    @abstractmethod
    def load(self) -> list:
        pass

    @abstractmethod
    def update_data(self, new_data: list) -> int:
        pass
