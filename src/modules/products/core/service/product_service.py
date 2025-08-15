from src.modules.products.core.repository.product_repository import ProductRepository

class ProductService(ProductRepository):

    async def get_all_products(self):
        return await super().get_all_products()

    async def add_new_product(self, product_data):
        return await super().add_new_product(product_data)

    async def get_by_id(self, product_id):
        return await super().get_by_id(product_id)

    async def update_product(self, product_id, user_data):
        return await super().update_product(product_id, user_data)

    async def delete_product(self, product_id):
        return await super().delete_product(product_id)