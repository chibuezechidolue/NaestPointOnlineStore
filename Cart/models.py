from django.db import models
from Product.models import Products
from User.models import CustomUser
import uuid

# Create your models here.

class Cart(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    session_id=models.CharField(max_length=150,null=True,blank=True)
    paid=models.BooleanField(default=False)
    date=models.DateField(auto_now=True)


    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def num_of_item(self):
        cart_items=self.cartitems.all()
        output=sum([item.quantity for item in cart_items])
        return output
    @property
    def total_cart_sum(self):
        cart_items=self.cartitems.all()
        output=sum([item.total_item_price for item in cart_items])
        return output



class CartItems(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitems')
    quantity=models.PositiveIntegerField(default=0)
    size=models.CharField(max_length=2,default="MD")

    def __str__(self) -> str:
        return self.product.product_name
    
    @property
    def total_item_price(self):
        product_price=self.product.product_price.replace(",","")
        return self.quantity*int(product_price)
        


class SavedItems(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    product=models.OneToOneField(Products,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.product

