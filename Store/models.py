from django.db import models
from django.contrib.postgres.fields import ArrayField

class Advertisement(models.Model):
    advert_title=models.CharField(max_length=100,default="no advert title")
    advert_text=models.CharField(max_length=250,default="no advert text")
    advert_location=models.CharField(max_length=150,choices=(
        ('Nav_advert', 'Nav_advert'),
        ('CAROUSEL', u'CAROUSEL'),
        ('sec2_advert', u'sec2_advert'),
        ('sec3_advert', u'sec3_advert'),
        ('sec4_advert', u'sec4_advert'),
        ('whats-hot_advert', 'whats-hot_advert'),))
    advert_img=models.ImageField(upload_to="images/advert",default="default_carousel.jpg")
    advert_url=models.URLField(max_length=500,blank=True,null=True)

class Collection(models.Model):
    collection_name=models.CharField(max_length=100,default="no name",unique=True)
    collection_description=models.TextField()
    collection_img_1=models.ImageField(upload_to="images/collection",default="default_collection.jpg",null=True)
    collection_img_2=models.ImageField(upload_to="images/collection",default="default_collection.jpg",null=True)
    collection_img_3=models.ImageField(upload_to="images/collection",default="default_collection.jpg",null=True)
    collection_img_4=models.ImageField(upload_to="images/collection",default="default_collection.jpg",null=True)
    collection_img_5=models.ImageField(upload_to="images/collection",default="default_collection.jpg",null=True)
    # collection = models.ForeignKey(Products, on_delete=models.CASCADE)

    
    def __str__(self) -> str:
        return self.collection_name


