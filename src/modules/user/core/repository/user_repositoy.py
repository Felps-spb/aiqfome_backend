from abc import ABC, abstractmethod
import uuid
class UserRepository(ABC):
    
    @abstractmethod
    async def get_all_users(self):
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str):
        pass

    @abstractmethod
    async def update_user(self, user_id: str, user_data):
        pass

    @abstractmethod
    async def delete_user(self, user_id: str):
        pass