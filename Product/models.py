from django.db import models
from Store.models import Collection

# Create your models here.

class Products(models.Model):
    product_name=models.CharField(max_length=150,unique=True)
    product_description=models.CharField(max_length=300)
    product_price=models.CharField(max_length=200)
    product_img_1=models.ImageField(upload_to=f"images/product",default="default.jpg")
    product_img_2=models.ImageField(upload_to=f"images/product",default="default.jpg",null=True)
    product_img_3=models.ImageField(upload_to=f"images/product",default="default.jpg",null=True)
    product_gender=models.CharField(max_length=50,choices=(
        ('1', u'MALE'),
        ('2', u'FEMALE'),
        ('3', u'KIDS'),
        ('4', u'ACCESSORIES'),
    ))
    prod_is_featured=models.BooleanField(default=False)
    # product_collection=models.CharField(max_length=200,default="unbranded")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,default=0)
    
    def __str__(self):
	    return self.product_name
    

class SocialMediaTag(models.Model):
    tag_handle=models.CharField(max_length=50)
    tag_url=models.URLField(null=True)
    tag_img=models.ImageField(upload_to=f"images/socialmedia",default="default.jpg")



