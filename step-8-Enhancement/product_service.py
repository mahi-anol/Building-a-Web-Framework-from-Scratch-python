from contants import products

class ProductService:
    def get_all_products(self)->list[dict]:
        return products
    def _get_product_by_id(self,product_id:int)->dict|None:
        for p in products:
            if p['id']==product_id:
                return p
        return None
    def create_new_product(self,product:dict)->list[dict]:
        products.append(product)
        return products

    def delete_product(self,product):
        products.remove(product)
        return products