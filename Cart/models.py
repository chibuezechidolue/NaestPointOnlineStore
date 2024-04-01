from django.db import models
from Product.models import Products
from User.models import CustomUser
import uuid

# Create your models here.

class Cart(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    paid=models.BooleanField(default=False)
    date=models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.id +  self.date


class CartItems(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartitems')
    quantity=models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.product.product_name
