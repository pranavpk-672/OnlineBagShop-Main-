from django.db import models

# Create your models here.
#model for product
class Product(models.Model):
    # Product Information Fields
    product_name = models.CharField(max_length=255)
    stock = models.IntegerField()
    about_product = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    capacity = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    material = models.CharField(max_length=255)

    # Product Images and Certificate Fields
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # You can add more image fields here if needed
    authentication_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    # Other fields and methods for your model as needed

    def __str__(self):
        return self.product_name