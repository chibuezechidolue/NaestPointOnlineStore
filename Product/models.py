from email.policy import default
from django.db import models
from Store.models import Collection
from django.contrib.postgres.fields import ArrayField

# Create your models here.
def get_default_choice():
    return ['MD']

class Products(models.Model):
    product_name=models.CharField(max_length=150,unique=True)
    product_description=models.CharField(max_length=300)
    product_price=models.CharField(max_length=200)
    product_sizes = ArrayField(
        models.CharField(max_length=2,blank=True),blank=True,default=get_default_choice
    )
    product_img_1=models.FileField(upload_to=f"images/product",default="default.jpg")
    product_img_2=models.FileField(upload_to=f"images/product",default="default.jpg",null=True)
    product_img_3=models.FileField(upload_to=f"images/product",default="default.jpg",null=True)
    product_gender=models.CharField(max_length=50,choices=(
        ('MALE', u'MALE'),
        ('FEMALE', u'FEMALE'),
        ('KIDS', u'KIDS'),
        ('ACCESSORIES', u'ACCESSORIES'),
    ))
    prod_is_featured=models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,default=0)
    
    def __str__(self):
	    return self.product_name
    

class SocialMediaTag(models.Model):
    tag_handle=models.CharField(max_length=50)
    tag_url=models.URLField(null=True)
    tag_img=models.FileField(upload_to=f"images/socialmedia",default="default.jpg")

    def __str__(self) -> str:
         return self.tag_handle



