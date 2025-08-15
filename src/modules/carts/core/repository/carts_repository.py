from abc import ABC, abstractmethod

class CartsRepository(ABC):
 
    @abstractmethod
    async def get_all_carts(self):
        pass

    @abstractmethod
    async def add_new_cart(self, cart_data: dict) -> dict:
        pass

    @abstractmethod
    async def get_by_id(self, cart_id: str):
        pass

    @abstractmethod
    async def update_cart(self, cart_id: str, user_data):
        pass

    @abstractmethod
    async def delete_cart(self, cart_id: str):
        pass
