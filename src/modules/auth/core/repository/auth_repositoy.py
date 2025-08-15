from abc import ABC, abstractmethod

class AuthRepository(ABC):
    @abstractmethod
    def register(self, user_data: dict) -> dict:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> dict:  
        pass