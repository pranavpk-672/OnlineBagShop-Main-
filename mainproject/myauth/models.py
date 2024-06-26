
# Create your models here.
from datetime import timezone
from django.db import models
from django.utils import timezone



from django.db import models
from django.conf import settings



# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        CUSTOMER="CUSTOMER",'Customer'
        DELIVERYBOY="DELIVERYBOY",'deliveryboy'
        SELLER="SELLER",'Seller'


    role = models.CharField(max_length=50,choices=Role.choices)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    alt_phone = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    pincode= models.CharField(max_length=6)  # You can adjust the max_length as needed
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    building_name = models.CharField(max_length=100)
    road_area = models.CharField(max_length=100)
    
    def _str_(self):
        return self.user.username
    
    #model for seller
# class SellerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15, unique=True)
#     alt_phone = models.CharField(max_length=12, unique=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
#     gst = models.CharField(max_length=15)
#     company_name = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=6)
#     state = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     address = models.CharField(max_length=255)
#     is_approved = models.BooleanField(default=False)
#     incorporation_certificate = models.FileField(upload_to='incorporation_certificates/', null=True, blank=True)
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    alt_phone = models.CharField(max_length=12, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gst = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=20, null=True, blank=True)  # Example length for latitude
    longitude = models.CharField(max_length=20, null=True, blank=True)  # Example length for longitude
    is_approved = models.BooleanField(default=False)
    incorporation_certificate = models.FileField(upload_to='incorporation_certificates/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name

#model for category
class category(models.Model):
    category_name = models.CharField(max_length=255)
    category_description = models.CharField(max_length=900)
    category_picture = models.ImageField(upload_to='category_pictures/', null=True, blank=True)
    category_verify = models.BooleanField(default=True)


#model for subcategory
class sub_category(models.Model):  
        sub_category_name = models.CharField(max_length=255)
        sub_category_description = models.CharField(max_length=900)
        sub_category_picture = models.ImageField(upload_to='category_pictures/', null=True, blank=True)
        sub_category_verify = models.BooleanField(default=True)
        category_id = models.ForeignKey(category, on_delete=models.DO_NOTHING, null=True, blank=True)

#model for product
class Product(models.Model):
    # Product Information Fields
    brand_name = models.CharField(max_length=255,null=True)
    product_name = models.CharField(max_length=255)
    product_number= models.CharField(max_length=100,unique=True,null=True)
    stock = models.IntegerField()
    about_product = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(category, on_delete=models.DO_NOTHING,null=True, blank=True)
    sub_category_id = models.ForeignKey(sub_category, on_delete=models.DO_NOTHING,null=True, blank=True)
    seller_id = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True, blank=True)
    capacity = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    material = models.CharField(max_length=255)       
    product_status = models.BooleanField(default=True)
    image_1 = models.ImageField(upload_to='product_main_images/', blank=True, null=True)

#model for images
class product_images(models.Model):  
    image_data = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, blank=True)


#model for cart

class Cart(models.Model):
    user           =     models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

class Cart_items(models.Model):
    user           =     models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product        =     models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    cart        =     models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    quantity       =     models.IntegerField(default=1)
    price       =     models.IntegerField(default=1)
    cart_verify    =     models.BooleanField(default=False)
    # id_number_info =     models.IntegerField(default=1)

    #MODEL FOR PAYMENT
class  user_payment(models.Model):
    user           =     models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    cart        =     models.IntegerField(blank=True, null=True)
    amount =     models.IntegerField(default=0)
    datetime = models.TextField(default="empty")
    order_id_data = models.TextField(default="empty")
    payment_id_data = models.TextField(default="empty")
   

#model for wishlist
class Wishlist(models.Model):
    user           =     models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product        =     models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)



#model for product review
class product_review(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_id = models.TextField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)
    product_rating = models.IntegerField()
    description = models.TextField(blank=True, null=True)  # Adding the description field



class DeliveryBoy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    delivery_zones = models.TextField()
    availability_timings = models.CharField(max_length=100)
    city = models.CharField(max_length=20, default='DefaultCity')
    state = models.CharField(max_length=20, default='DefaultState')
    pincode = models.PositiveIntegerField(default=0)  # Set a default value here
    address = models.TextField()
    has_updated_password = models.BooleanField(default=False)  # New field to track password update




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_date = models.DateField(auto_now_add=True)


    # You can add more image fields here if needed

    # Other fields and methods for your model as needed

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=8, unique=True)
    discount_percentage = models.PositiveIntegerField()
    seller_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    visibility = models.BooleanField(default=True)
    expiration_date = models.DateField(default='2099-12-31')  # Manually defining default value


class CouponUsed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_id = models.ForeignKey(Coupon, on_delete=models.CASCADE)

      
class Order(models.Model):
    userpayment = models.ForeignKey(user_payment, on_delete=models.CASCADE, null=True, blank=True)


class DeliveryAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='PENDING')



    def _str_(self):
        return f"DeliveryAssignment - {self.order} - {self.delivery_boy} - {self.status}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class PaymentData(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
       
    

class DeliveryOTP(models.Model):
    assignment = models.ForeignKey(DeliveryAssignment, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # Assuming OTP length is 6 characters





class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=100)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Assuming discount rate is a decimal value
    start_date = models.DateField()
    end_date = models.DateField()


    

def __str__(self):
        return f"Coupon: {self.coupon_code}, Discount: {self.discount_percentage}%"

   

   
   

    
    