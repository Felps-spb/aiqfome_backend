from src.modules.user.core.repository.user_repositoy import UserRepository


class UserService(UserRepository):
   
    async def get_all_users(self):
        return await super().get_all_users()

    async def get_user_by_id(self, user_id: int):
        return super().get_user_by_id(user_id)
    
    async def update_user(self, user_id: int, user_data):
        return super().update_user(user_id, user_data)
    
    async def delete_user(self, user_id: int): 
        return super().delete_user(user_id)