from src.modules.auth.core.repository.auth_repositoy import AuthRepository

class AuthService(AuthRepository):
    
    def register(self, user_data: dict) -> dict:
        return super().register(user_data)

    def login(self, username: str, password: str) -> dict:
        return super().login(username, password)