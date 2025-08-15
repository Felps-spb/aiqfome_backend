from abc import ABC, abstractmethod

class ProductRepository(ABC):

    @abstractmethod
    async def get_all_products(self):
        pass

    @abstractmethod
    async def add_new_product(self, product_data: dict) -> dict:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str):
        pass

    @abstractmethod
    async def update_product(self, product_id: str, user_data):
        pass

    @abstractmethod
    async def delete_product(self, product_id: str):
        pass
