from src.modules.carts.core.repository.carts_repository import CartsRepository

class CartsService(CartsRepository):

    async def get_all_carts(self):
        return await super().get_all_carts()
    
    async def add_new_cart(self, cart_data):
        return await super().add_new_cart(cart_data)
    
    async def get_by_id(self, cart_id):
        return await super().get_by_id(cart_id)
    
    async def update_cart(self, cart_id, user_data):
        return await super().update_cart(cart_id, user_data)
    
    async def delete_cart(self, cart_id):
        return await super().delete_cart(cart_id)
    