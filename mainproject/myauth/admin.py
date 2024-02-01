from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, SellerProfile, Product, product_images,Cart,Wishlist,product_review,Cart_items

class CustomUserAdmin(UserAdmin):
 #   list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
  #  list_filter = ('is_staff', 'is_active')
   # search_fields = ('username', 'email', 'first_name', 'last_name')
    
    def get_queryset(self, request):
        # Exclude superusers from the admin table
        return User.objects.exclude(is_superuser=True)

# Register your custom user model with the custom admin
admin.site.register(User, CustomUserAdmin),
admin.site.register(Profile),



admin.site.register(SellerProfile),
admin.site.register(Cart),
admin.site.register(Cart_items),
admin.site.register(Product),
admin.site.register(Wishlist),
admin.site.register(product_review),
admin.site.register(product_images)






