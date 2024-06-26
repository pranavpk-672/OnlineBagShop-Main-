from collections import Counter
import datetime
from email.headerregistry import Address
import io
from itertools import count
import json
from multiprocessing import context
import random
import string
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from numpy import count_nonzero
import pandas as pd
from django.contrib.auth.hashers import make_password
import qrcode
from requests import request
from .models import DeliveryBoy
# from .forms import DeliveryBoyForm
from .models import Notification

from django.db.models.functions import Left
from django.db.models import Count, Max
from django.db.models import Q




import razorpay
from django.http import HttpResponseBadRequest, JsonResponse
from django.core import serializers
from django.db.models import Q
from .models import User
from .models import *
from django.db.models import Subquery, OuterRef
from .models import category


from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import F

from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect

from django.views.generic import View

from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import DjangoUnicodeDecodeError
import re
from django.core.mail import EmailMessage

from django.views.generic import View
from django.core.mail import EmailMessage

from .models import Product, category, sub_category, product_images, product_review, Cart_items


#from .utils import *
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
# getting token from utils.py
from .utils import TokenGenerator,generate_token
#emails
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
#threading
import threading
#activation and deactivation
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import render
from .models import Profile

from django.core.mail import EmailMessage

from .models import Product, Profile, SellerProfile

from .models import SellerProfile
from django.shortcuts import render
from .models import SellerProfile

from .models import Product  # Import your Product model here
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Cart
from .models import Wishlist


from django.shortcuts import render, redirect
from .models import Product, Cart


# try:
#     import razorpay
# except ImportError:
#     # Handle the ImportError as needed
#     razorpay = None

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        super().__init__()  #Call the parent class's __init__ method

    def run(self):
        self.email_message.send()

# Create your views here.

def signup(request):
    if request.method == "POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'auth/signup.html')

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'auth/signup.html')
        except Exception as identifier:
            pass

        myuser = User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=email,role='CUSTOMER')
        
        
        #authentication
        myuser.is_active=False

        myuser.save()
        #authentication
        current_site=get_current_site(request)
        email_subject="Activate your Account"
        message=render_to_string('auth/activate.html',{
             'User':myuser,
             'domain':'127.0.0.1:8000',
             'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
             'token':generate_token.make_token(myuser)
             
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        




        messages.info(request, " Activate your account by clicking link on your email")
        return redirect('/myauth/login')

    return render(request, 'auth/signup.html',)
#login
def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['password']
        myuser=authenticate(username=username,password=userpassword)

       # if myuser is not None:
          #  login(request,myuser)
         #   #messages.success(request,"Login Success")
        #    return render(request,'index.html')
       # else:
      #      messages.error(request,"Invalid credential")
     #       return redirect('/myauth/login')
    #return render(request,'auth/login.html')


        if myuser is not None:
                login(request,myuser)
               # messages.success(request,"Login Success")
                #request.session['email']=myuser.email

                #session
                request.session['username']=username




                if myuser.role=='CUSTOMER':
                        #messages.success(request,"Login Sucess!!!")
                        return redirect('home')
                elif myuser.role=='SELLER':
                        #messages.success(request,"Login Sucess!!!")
                        return redirect('seller_dashboard')
                elif myuser.role=='ADMIN':
                          
                          return redirect('adminreg')
                elif myuser.role=='DELIVERYBOY':
                          
                          return redirect('delivery_login')
                          
        else:
                messages.error(request,"Invalid credential")
                return redirect('/myauth/login')
    #return render(request,'auth/login.html')

   #session
    response = render(request,'auth/login.html')
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response


#delivery signup
def log(request):
    
    return render(request,'auth/log.html')



#logout
def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/myauth/login')


login_required
def home(request):
      
      if 'username' in request.session:
        items = Product.objects.all()[:12]
        categories = category.objects.all()
        subcategories = sub_category.objects.all()

#starting count code
        user = request.user
        user_cartd = Cart.objects.filter(user=user)
        total_cart_items_count = 0
        for user_cart in user_cartd:
            cart_items_count = Cart_items.objects.filter(cart=user_cart, cart_verify=False).count()
            total_cart_items_count += cart_items_count
#ending count code
        # cart_items_count = Cart.objects.filter(user=request.user, cart_verify=True).count()

        response = render(request, 'home.html', {'items': items, 'cart_items_count': total_cart_items_count, 
                                                 'categories': categories, 'subcategories': subcategories})
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
      else:
        return redirect('/myauth/login')
        #return render(request,'home.html')



        #sellerlogin
def sellersig(request):
       if 'username' in request.session:
        response = render(request,'sellersign.html')
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
       else:
        return redirect('/myauth/login')
@never_cache
@login_required(login_url="handlelogin")
#admin dashboard
def adminreg(request):
    # Query all User objects (using the custom user model) from the database

    customer_count = User.objects.filter(role='CUSTOMER').count()
    seller_count = User.objects.filter(role='SELLER').count()
    delivery_boy_count = User.objects.filter(role='DELIVERYBOY').count()

    approvcount = SellerProfile.objects.filter().count()
    productcount = Product.objects.filter().count()
    notificationcount = Notification.objects.filter().count()
    

    # Get the last three users from the notifications table
    last_three_notifications = Notification.objects.order_by('-id')[:3]
    last_three_users = [{'username': notification.user.username, 'current_date': notification.current_date, 'name': f"{notification.user.first_name} {notification.user.last_name}"} for notification in last_three_notifications]

    # Pass the counts and last three users to the template context
    context = {
        'customer_count': customer_count,
        'seller_count': seller_count,
        'delivery_boy_count': delivery_boy_count,
        'last_three_users': last_three_users,
        'approvcount': approvcount,
        'productcount' : productcount,
        'notificationcount' : notificationcount
    }
    
    # Render the HTML template
    return render(request, 'admintemplate.html', context)



#authentication
class ActivateAccountView(View):
     def get(self,request,uidb64,token):
          try:
               uid=force_bytes(urlsafe_base64_decode(uidb64))
               myuser=User.objects.get(pk=uid)
          except Exception as identifier:
               myuser=None
          if myuser is not None and generate_token.check_token(myuser,token):
               myuser.is_active=True
               myuser.save()
               messages.info(request,"Account Activated Successfully")
               return redirect('/myauth/login')
          return render(request,'auth/activatefail.html')  


#user view
@login_required     
def adminn(request):
    User = get_user_model()
    user_profiles = User.objects.filter(role='CUSTOMER')
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request,'userview.html',context)

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('activation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('/myauth/adminn/')

def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivat the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('deactivation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('/myauth/adminn/')



#userview2
def userviewss(request):
    # Retrieve customer profiles with the role 'CUSTOMER'
    user_profiles = Profile.objects.filter(user__role='CUSTOMER')
    print(user_profiles)
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request, 'userviews.html', context)




#about
def abouttt(request):

    return render(request, 'about.html' )
#contact
def con(request):

    return render(request, 'contact.html' )
#updateprofilr
def updateprofile(request):
    
   return render(request,'auth/updateprofile.html')


#updateprofile

def update_profile(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        altphone = request.POST['alt_phone']
        img = request.FILES.get('profile_picture')
        pin = request.POST['pincode']
        statee = request.POST['state']
        cityy = request.POST['city']

        housename = request.POST['building_name']
        roadname = request.POST['road_area']
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('update-profile')  # Redirect to the same page with the warning message

        # Validate phone
        if Profile.objects.filter(phone=phone).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('update-profile')  # Redirect to the same page with the warning message

        
        
        if email != request.user.email:
            user=request.user
            user.email=email
            user.username=email
            user.is_active=False  #make the user inactive
            user.save()
            
            
            current_site=get_current_site(request)  
            email_subject="Activate your account"
            message=render_to_string('auth/activate.html',{
                   'user':user,
                   'domain':current_site.domain,
                   'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                   'token':generate_token.make_token(user)


            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.info(request,"Active your account by clicking the link send to your email")
            logout(request)
           
            return redirect('/myauth/login')
            
        
        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username=email
        user.email = email
        user.save()
        
        # Update the Profile model fields
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = phone
        profile.alt_phone = altphone
        profile.profile_picture = img
        profile.pincode = pin
        profile.state = statee
        profile.city = cityy
        profile.building_name = housename
        profile.road_area = roadname
        profile.save()
        

        # Logout the user and redirect to the signup page
        messages.success(request,'profile updated')
        return redirect('home')
    else:
        return render(request, 'auth/updateprofile.html', {'user': request.user})
    
    #seller signup
def sell(request):
    
    return render(request,'auth/seller_signup.html')



#seller signup
# def signupsell(request):
#     if request.method == "POST":
#         fname=request.POST['first_name']
#         lname=request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         if password != confirm_password:
#             messages.warning(request, "Password is not matching")
#             return render(request, 'auth/seller_signup.html')

#         try:
#             if User.objects.get(username=email):
#                 messages.warning(request, "Email is already taken")
#                 return render(request, 'auth/seller_signup.html')
#         except Exception as identifier:
#             pass

#         myuser = User.objects.create_user(first_name=fname,last_name=lname,email=email,password=password,username=email,role='SELLER')
#         print(myuser)

#         #authentication
#         myuser.is_active=False

#         myuser.save()
#         #authentication
#         current_site=get_current_site(request)
#         email_subject="Activate your Account"
#         message=render_to_string('auth/activate.html',{
#              'User':myuser,
#              'domain':'127.0.0.1:8000',
#              'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
#              'token':generate_token.make_token(myuser)
             
#         })
#         email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
#         EmailThread(email_message).start()

#         messages.info(request, " Activate your account by clicking link on your email")
#         return redirect('/myauth/login')

#     return render(request, 'auth/seller_signup.html')

def signupsell(request):
    if request.method == "POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.warning(request, "Password is not matching")
            return render(request, 'auth/seller_signup.html')

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'auth/seller_signup.html')
        except Exception as identifier:
            pass

        # Create the user
        myuser = User.objects.create_user(first_name=fname, last_name=lname, email=email, password=password, username=email, role='SELLER')
        myuser.is_active=False
        myuser.save()

        # Create a notification for the user
        Notification.objects.create(user=myuser)

        # Send activation email
        current_site=get_current_site(request)
        email_subject="Activate your Account"
        message=render_to_string('auth/activate.html', {
             'User':myuser,
             'domain':'127.0.0.1:8000',
             'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
             'token':generate_token.make_token(myuser)
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()

        messages.info(request, "Activate your account by clicking link on your email")
        return redirect('/myauth/login')

    return render(request, 'auth/seller_signup.html')


#update_seller_profile

def seller_profile_update(request):
    if request.method == 'POST':
        # Process the form data and update the user's profile
        # Retrieve form fields
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        altphone = request.POST['alt_phone']
        #img = request.POST['profile_picture']
        img = request.FILES.get('profile_picture')
        certificate = request.FILES.get('incorporation_certificate')

        gst = request.POST['gst']
        pin = request.POST['pincode']
        state = request.POST['state']
        city = request.POST['city']
        address = request.POST.get('address')
        company_name = request.POST.get('company_name')
        country = request.POST.get('country')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        # Check if the email is already taken by another user
        if User.objects.filter(username=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email is already taken")
            return redirect('sell_upd')  # Redirect to the same page with the warning message

        # Validate phone number
        if Profile.objects.filter(phone=phone).exclude(user=request.user).exists():
            messages.warning(request, "Phone number is already taken")
            return redirect('sell_upd')  # Redirect to the same page with the warning message

        # If the email is different from the current user's email, update the email and send an activation email
        if email != request.user.email:
            user = request.user
            user.email = email
            user.username = email
            user.is_active = False  # Make the user inactive
            user.save()
            
            current_site = get_current_site(request)  
            email_subject = "Activate your account"
            message = render_to_string('auth/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            EmailThread(email_message).start()
            messages.info(request, "Activate your account by clicking the link sent to your email")
            logout(request)
            return redirect('/myauth/login')

        # Update the User model fields
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = email
        user.email = email
        user.save()
        
        # Update the SellerProfile model fields
        seller_profile, created = SellerProfile.objects.get_or_create(user=user)
        seller_profile.phone = phone
        seller_profile.alt_phone = altphone
        seller_profile.profile_picture = img
        seller_profile.incorporation_certificate = certificate

        seller_profile.pincode = pin
        seller_profile.state = state
        seller_profile.city = city
        seller_profile.company_name = company_name
        seller_profile.country = country
        seller_profile.address = address
        seller_profile.gst = gst
        seller_profile.latitude = lat
        seller_profile.longitude = lon
        seller_profile.save()

        # Logout the user and redirect to the seller profile update page
        messages.success(request, 'Profile updated  and Approval is pending')
        return redirect('/myauth/login')
    else:
        # Render the seller profile update page
        return render(request, 'sellersign.html', {'user': request.user})



#seller view
@login_required
def sellerr(request):
    User = get_user_model()
    user_profiles = User.objects.filter(role='SELLER')
    
    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request,'seller_view.html',context)

def activate_seller(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    subject = 'Account Activation'
    html_message = render_to_string('activation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    return redirect('/myauth/sellerr/')

def deactivate_seller(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_superuser:
        return HttpResponse("You cannot deactivat the admin.")
    user.is_active = False
    user.save()
    subject = 'Account Deactivation'
    html_message = render_to_string('deactivation_mail.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = 'hsree524@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    # Send an email to the user here
    return redirect('/myauth/sellerr/')

#sellerview2
def sellviews(request):
    # Retrieve seller profiles with the role 'SELLER'
    user_profiles = SellerProfile.objects.filter(user__role='SELLER')

    # Pass the data to the template
    context = {'user_profiles': user_profiles}
    return render(request, 'seller_viewss.html', context)


#seller approval
def sellor_approval(request):
    #unapproved_sellers = SellerProfile.objects.filter(is_approved=False)
    unapproved_sellers = SellerProfile.objects.all()

    
    return render(request,'pending_seller_activation.html',{'unapproved_sellers': unapproved_sellers})



def approve_seller(request, seller_id):
    seller = SellerProfile.objects.get(pk=seller_id)
    seller.is_approved = True
    seller.save()
    subject = 'Your Seller Account Has Been Approved'
    message = 'Dear {},\n\nYour seller account has been approved by the admin. You can now log in and start using your account.\n\nLogin Link: http://127.0.0.1:8000/auth_app/handlelogin/'.format(seller.user.first_name)
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [seller.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return redirect('sellor_approval')

#block_seller - to block the seller approvel
def block_seller(request, seller_id):
    seller = SellerProfile.objects.get(pk=seller_id)
    seller.is_approved = False
    seller.save()
    subject = 'Your Seller Account Has Been blocked'
    message = 'Dear {},\n\nYour seller account has been blocked by the admin. You cannot  log in and  banned your account.'
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [seller.user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    return redirect('sellor_approval')

#delete_seller  -to delete seller 
def delete_seller(request, seller_id):
   
    user =User.objects.get(pk=seller_id)
    user.delete()
    subject = 'Your Seller Account Has Been deleted'
    message = 'Dear {},\n\nYour seller account has been deleted by the admin. You cannot  log in and  banned your account.'
    from_email = 'prxnv2832@gmail.com'  # Replace with your email address
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('sellor_approval')

# @never_cache
# @login_required(login_url="handlelogin")
# #seller approval
# def seller_dashboard(request):
#     try:
#         seller_profile = request.user.sellerprofile
#         if seller_profile.is_approved:
#             return render(request, 'seller_dashboard.html')
#         else:
#             messages.success(request, 'Your profile is pending admin approval.')
#             return redirect('sellersig')  # Redirect to the sellersign view
#     except SellerProfile.DoesNotExist:
#         messages.success(request, 'You do not have a seller profile.')
#         return redirect('sellersig')


@never_cache
@login_required(login_url="handlelogin")
#seller approval
def seller_dashboard(request):
    try:
        seller_profile = request.user.sellerprofile
        if seller_profile.is_approved:
            # Get count of total products under the seller
            total_products = Product.objects.filter(seller_id=request.user).count()

            # Get top selling products
            top_selling_products = Product.objects.filter(seller_id=request.user)\
                .annotate(total_sold=Count('cart_items'))\
                .order_by('-total_sold')[:6]

            # Get last sold product and its purchased quantities
            last_sold_product = Product.objects.filter(seller_id=request.user)\
                .annotate(last_sold=Max('cart_items__id'))\
                .order_by('-last_sold').first()

            # Get purchased quantities of the last sold product
            if last_sold_product:
                purchased_quantities = Cart_items.objects.filter(product=last_sold_product).count()
            else:
                purchased_quantities = 0

            seller_products = Product.objects.filter(seller_id=request.user)

            # Get cart items sold by the seller
            seller_cart_items_ids = Cart_items.objects.filter(product__in=seller_products).values_list('id', flat=True)

            # Get carts containing seller's items
            seller_carts = Cart.objects.filter(cart_items__id__in=seller_cart_items_ids)

            # Get total amount from user payments for seller's carts
            total_amount = user_payment.objects.filter(cart__in=seller_carts).aggregate(total_amount=Sum('amount'))['total_amount'] or 0



            seller_products = Product.objects.filter(seller_id=request.user)

            # Get cart items sold by the seller
            seller_cart_items_ids = Cart_items.objects.filter(product__in=seller_products).values_list('id', flat=True)

            # Get carts containing seller's items
            seller_carts = Cart.objects.filter(cart_items__id__in=seller_cart_items_ids)

            # Get total purchases of seller's products from user payments
            total_purchases_user_payments = user_payment.objects.filter(cart__in=seller_carts).count()
            # Get one product with stock less than or equal to 2
            low_stock_product = Product.objects.filter(seller_id=request.user, stock__lte=2).first()

            context = {
                'total_products': total_products,
                'top_selling_products': top_selling_products,
                'last_sold_product': last_sold_product,
                'purchased_quantities': purchased_quantities,
                'total_amount': total_amount,
                'total_purchases_user_payments': total_purchases_user_payments,
                'low_stock_product': low_stock_product
            }
            return render(request, 'seller_dashboard.html', context)
        else:
            messages.success(request, 'Your profile is pending admin approval.')
            return redirect('sellersig')  # Redirect to the sellersign view
    except SellerProfile.DoesNotExist:
        messages.success(request, 'You do not have a seller profile.')
        return redirect('sellersig')




 #seller add product
def selleraddprod(request):
    
    return render(request,'seller_add_prod.html')


# add category
def add_category(request):
    if request.method == 'POST':
        # Retrieve form data from the request
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        category_picture = request.FILES.get('category_picture')

        # Create a new Category instance
        new_category = category(
            category_name=category_name,
            category_description=category_description,
            category_verify=1,  # Convert the string to a boolean
            category_picture=category_picture
        )

        # Save the category instance to the database
        new_category.save()

        # Redirect to a success page or do something else
        return redirect('category_list') # Adjust this as needed
    else:
        return render(request, 'category_add.html')

# list categories

def category_list(request):
    categories = category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def delete_category(request, category_id):
    # Use a different name for the variable holding the instance
    category_instance = get_object_or_404(category, id=category_id)

    if request.method == 'POST':
        category_instance.delete()

    return redirect('category_list')


def add_sub_category(request, category_id):
    
    try:
        category_instance = category.objects.get(id=category_id)
    except category.DoesNotExist:
        return JsonResponse({'error': 'Category does not exist'}, status=404)

    categories = category.objects.all()  # Fetch all categories for the select options

    if request.POST.get('type'):
        sub_category_name = request.POST.get('sub_category_name')
        sub_category_description = request.POST.get('sub_category_description')
        sub_category_picture = request.FILES.get('sub_category_picture')

        try:
            # Create and save the SubCategory instance
            sub_category_instance = sub_category(
                sub_category_name=sub_category_name,
                sub_category_description=sub_category_description,
                sub_category_picture=sub_category_picture,
                sub_category_verify=1,
                category_id_id=category_id  # Assuming category_id is a ForeignKey in SubCategory
            )
            sub_category_instance.save()
            print("SubCategory saved successfully:", sub_category_instance)
        except Exception as e:
            error_message = f"Error saving SubCategory: {str(e)}"
            print(error_message)
            return JsonResponse({'error': error_message}, status=500)


    return render(request, 'SubCategoryAdd.html', {'category_instance': category_instance, 'categories': categories})


# list sub categories
def sub_category_list(request, category_id):
    subcategories = sub_category.objects.filter(category_id=category_id)
    return render(request, 'sub_category_list.html', {'subcategories': subcategories})

# delete sub category
def delete_sub_category(request, sub_category_id):
    #return JsonResponse({"id data ": sub_category_id})
    # Use a different name for the variable holding the instance
    sub_category_instance = get_object_or_404(sub_category, id=sub_category_id)

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        sub_category_instance.delete()

    return redirect('sub_category_list', category_id=category_id)



#product add
def add_product(request):

    categories = category.objects.all()
    subcategories = sub_category.objects.all()

    if request.method == 'POST':
        product_name = request.POST['product_name']
        brand_name = request.POST['brand_name']
        product_number = request.POST['product_number']
        stock = request.POST['stock']
        about_product = request.POST['about_product']
        current_price = request.POST['current_price']
        category_id = request.POST['category_id']
        sub_category_id = request.POST['sub_category_id']
        seller_id = request.user  # Assuming you are using the built-in User model for authentication
        capacity = request.POST['capacity']
        color = request.POST['color']
        material = request.POST['material']
        image1 = request.FILES['main_image']

        product = Product.objects.create(
            product_name=product_name,
            brand_name=brand_name,
            product_number=product_number,
            stock=stock,
            about_product=about_product,
            current_price=current_price,
            category_id_id=category_id,
            sub_category_id_id=sub_category_id,
            seller_id=seller_id,
            capacity=capacity,
            color=color,
            material=material,
            image_1=image1
        )

        # Handling product images
        for i in range(1, int(request.POST['num_images']) + 1):
            image_data = request.FILES.get(f'image_{i}')

            if image_data:
                product_images.objects.create(image_data=image_data, product_id=product)

        return redirect('seller_dashboard')  # Redirect to a product list page or any other page after successful submission

    return render(request, 'add_product.html', {'categories': categories, 'subcategories': subcategories})





# def add_product(request):
#     if request.method == 'POST':
#         # Retrieve data from the form
#         stock = request.POST.get('stock')
#         capacity = request.POST.get('capacity')
#         color = request.POST.get('color')
#         material = request.POST.get('material')


#         category = request.POST.get('category')
#         sub_category = request.POST.get('sub_category')
#         product_name = request.POST.get('product_name')
#         current_price = request.POST.get('current_price')
#         about_product = request.POST.get('about_product')
#         # Retrieve images and certificate
#         image1 = request.FILES['image1']
#         image2 = request.FILES.get('image2')
#         image3 = request.FILES.get('image3')
#         # Uncomment these lines if you plan to use image4 and authentication_certificate
#         # image4 = request.FILES.get('image4')
#         authentication_certificate = request.FILES['authentication_certificate']

#         # Create a new Product instance and save it
#         product = Product(
#             category=category,
#             sub_category=sub_category,
#             product_name=product_name,
#             current_price=current_price,
#             stock=stock,
#             color=color,
#             capacity=capacity,
#             material=material,
#             about_product=about_product,

#             image1=image1,
#             image2=image2,
#             image3=image3,
#             # image4=image4,  # Uncomment if needed
#              authentication_certificate=authentication_certificate,  # Uncomment if needed
#         )

#         # Assuming you have a 'seller' field in your Product model to associate the seller
#         product.seller = request.user.sellerprofile
        

#         product.save()
#         messages.success(request, "Product added successfully. Waiting for approval.")
#         return redirect('seller_dashboard')
    
#     return render(request, 'seller_add_prod.html')


# def index(request):
#     items = Product.objects.all()
#     return render(request, '.html',{'items': items})




#product detailed view
    
# def prodetailview(request, product_id):

#     subcategory_id = request.GET.get('subcat_id')


#     product = Product.objects.get(id=product_id)
#     product_images = product.product_images_set.all()  # Accessing related images via reverse relation

#     similar_products = Product.objects.filter(sub_category_id=subcategory_id).exclude(id=product_id)[:5]
    
#     return render(request, 'product_detailed_view.html', {'product': product, 'product_images': product_images,
#                                                           'similarproducts': similar_products})

def prodetailview(request, product_id):
    subcategory_id = request.GET.get('subcat_id')

    product = Product.objects.get(id=product_id)
    product_images = product.product_images_set.all()

    categories = category.objects.all()
    subcategories = sub_category.objects.all()
    cart_items_count = Cart_items.objects.filter(user=request.user, cart_verify=False).count()


    similar_products = Product.objects.filter(sub_category_id=subcategory_id).exclude(id=product_id)[:6]

    reviews = product_review.objects.filter(product_id=product_id)  # Filter reviews by product_id

    review_details = []
    for review in reviews:
        review_details.append({
            'review_text': review.description,
            'rewview_rating': review.product_rating,
            'username': review.user.first_name,
            'dateinfo': review.created_at
        })

    return render(request, 'product_detailed_view.html', {
        'product': product,
        'product_images': product_images,
        'similarproducts': similar_products,
        'reviews': review_details,'cart_items_count': cart_items_count, 
                                                 'categories': categories, 'subcategories': subcategories
    })



def prodetailview_index(request, product_id):
    subcategory_id = request.GET.get('subcat_id')

    product = Product.objects.get(id=product_id)
    product_images = product.product_images_set.all()

    categories = category.objects.all()
    subcategories = sub_category.objects.all()


    similar_products = Product.objects.filter(sub_category_id=subcategory_id).exclude(id=product_id)[:6]

    reviews = product_review.objects.filter(product_id=product_id)  # Filter reviews by product_id

    review_details = []
    for review in reviews:
        review_details.append({
            'review_text': review.description,
            'rewview_rating': review.product_rating,
            'dateinfo': review.created_at
        })

    return render(request, 'product_detailed_view.html', {
        'product': product,
        'product_images': product_images,
        'similarproducts': similar_products,
        'reviews': review_details, 
                                                 'categories': categories, 'subcategories': subcategories
    })

#ALL product  view
def productallview(request):
    items = Product.objects.all()
    categories = category.objects.all()
    subcategories = sub_category.objects.all()
    cart_items_count = Cart_items.objects.filter(user=request.user, cart_verify=False).count()


    
    return render(request,'product_view.html',{'items': items ,'cart_items_count': cart_items_count, 
                                                 'categories': categories, 'subcategories': subcategories})





def productcategorylistview(request, category_id):
    items = Product.objects.filter(category_id=category_id)
    # subcategories = sub_category.objects.filter(category_id=category_id)

    categories = category.objects.all()
    subcategories = sub_category.objects.all()
    cart_items_count = Cart_items.objects.filter(user=request.user, cart_verify=False).count()
    
    return render(request, 'product_by_category.html', {'items': items, 'cart_items_count': cart_items_count, 
                                                 'categories': categories, 'subcategories': subcategories})


def productsubcategorylistview(request, subcategory_id):
    items = Product.objects.filter(sub_category_id=subcategory_id)

    categories = category.objects.all()
    subcategories = sub_category.objects.all()
    cart_items_count = Cart_items.objects.filter(user=request.user, cart_verify=False).count()
    
    return render(request, 'sub_category_view.html', {'items': items,'cart_items_count': cart_items_count, 
                                                 'categories': categories, 'subcategories': subcategories})

#cart  view

def cartt(request):
    
    
    return render(request,'cart.html')


#Admin view products
@login_required

def admin_prodview(request):
    # Retrieve all products by default
    products = Product.objects.all()

    # Handling search functionality
    query = request.GET.get('q')
    if query:
        # Filter products by product_name containing the query string
        products = products.filter(product_name__icontains=query)

    # Handling filter functionality
    # You can add more filter options as needed
    filters = {}
    category_name = request.GET.get('category')
    subcategory_name = request.GET.get('subcategory')
    brand_name = request.GET.get('brand')  # Added for brand filtering
    if category_name:
        # Filter products by category name
        products = products.filter(category_id__category_name=category_name)
        filters['category'] = category_name
    if subcategory_name:
        # Filter products by subcategory name
        products = products.filter(category_id__sub_category__sub_category_name=subcategory_name)
        filters['subcategory'] = subcategory_name
    if brand_name:
        # Filter products by brand name
        products = products.filter(brand_name=brand_name)
        filters['brand'] = brand_name

    # Pass distinct category names, subcategory names, and brand names to the template for the dropdown menus
    distinct_categories = category.objects.values_list('category_name', flat=True).distinct()
    # distinct_subcategories = SubCategory.objects.values_list('sub_category_name', flat=True).distinct()
    distinct_brands = Product.objects.values_list('brand_name', flat=True).distinct()

    # Pass the filter options to the template
    context = {
        'products': products,
        'filters': filters,
        'distinct_categories': distinct_categories,
        # 'distinct_subcategories': distinct_subcategories,
        'distinct_brands': distinct_brands,
    }

    return render(request, 'admin_view_product.html', context)



# def admin_prodview(request):
#      products = Product.objects.all()
#      return render(request, 'admin_view_product.html', {'products': products})

# def admin_prodview(request):
#     # Retrieve all products by default
#     products = Product.objects.all()

#     # Handling search functionality
#     query = request.GET.get('q')
#     if query:
#         # Filter products by product_name containing the query string
#         products = products.filter(product_name__icontains=query)

#     # Handling filter functionality
#     # You can add more filter options as needed
#     filters = {}
#     category = request.GET.get('category')
#     if category:
#         products = products.filter(category_id=category)
#         filters['category'] = category

#     # Pass the filter options to the template
#     context = {
#         'products': products,
#         'filters': filters,
#     }

#     return render(request, 'admin_view_product.html', context)


#Admin view products
@login_required
# def admin_proddview(request):
#      products = Product.objects.all()
#      return render(request, 'review.html', {'products': products})
@login_required
def admin_proddview(request):
    # Retrieve all products by default
    products = Product.objects.all()

    # Handling search functionality
    query = request.GET.get('q')
    if query:
        # Filter products by product_name containing the query string
        products = products.filter(product_name__icontains=query)

    # Handling filter functionality
    # You can add more filter options as needed
    filters = {}
    category_name = request.GET.get('category')
    subcategory_name = request.GET.get('subcategory')
    brand_name = request.GET.get('brand')  # Added for brand filtering
    if category_name:
        # Filter products by category name
        products = products.filter(category_id__category_name=category_name)
        filters['category'] = category_name
    if subcategory_name:
        # Filter products by subcategory name
        products = products.filter(category_id__sub_category__sub_category_name=subcategory_name)
        filters['subcategory'] = subcategory_name
    if brand_name:
        # Filter products by brand name
        products = products.filter(brand_name=brand_name)
        filters['brand'] = brand_name

    # Pass distinct category names, subcategory names, and brand names to the template for the dropdown menus
    distinct_categories = category.objects.values_list('category_name', flat=True).distinct()
    # distinct_subcategories = SubCategory.objects.values_list('sub_category_name', flat=True).distinct()
    distinct_brands = Product.objects.values_list('brand_name', flat=True).distinct()

    # Pass the filter options to the template
    context = {
        'products': products,
        'filters': filters,
        'distinct_categories': distinct_categories,
        # 'distinct_subcategories': distinct_subcategories,
        'distinct_brands': distinct_brands,
    }

    return render(request, 'review.html', context)

#seller view products
# def seller_prodview(request):
#      products = Product.objects.all()
#      return render(request, 'seller_product_view.html', {'products': products})

def seller_prodview(request):
    products = Product.objects.filter(seller_id=request.user)
    return render(request, 'seller_product_view.html', {'products': products})


# def update_product(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     if request.method == 'POST':
#         new_stock = request.POST.get('stock')
#         product.stock = new_stock
#         product.save()
#         return redirect('seller_prodview')
#     return render(request, 'seller_product_view.html', {'products': [product]})
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        new_stock = request.POST.get('stock')
        product.stock = new_stock
        product.save()
        messages.success(request, 'Stock updated successfully!')
        return HttpResponseRedirect(request.path_info + '?success=true')
    return render(request, 'seller_product_view.html', {'products': [product]})

     

def category_detail(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def subcategory_detail(request, category):
    products = Product.objects.filter(sub_category=category)
   
    return render(request, 'sub_category_view.html', {'category': category, 'products': products,})


def brand_detail(request, category):
    products = Product.objects.filter(product_name=category)
    return render(request, 'brand_view.html', {'category': category, 'products': products})


 #category add
def category_add(request):
    
    return render(request,'CategoryAdd.html')


     #sub category add
def subcategory_add(request):
    
    return render(request,'SubCategoryAdd.html')



# view for cart
@never_cache
def add_to_cart(request, product_id):
    # Get the product or return product_not_found page
    product = get_object_or_404(Product, id=product_id)

    quantity = request.POST.get('quantity', 1)
    if not quantity:
        quantity = 1

    # Check if the product already exists in the user's cart with cart_verify=False
    cart_item = Cart_items.objects.filter(
        user=request.user, product=product, cart__cart_items__cart_verify=False
    ).first()

    if cart_item:
        # If the item already exists and cart_verify=False, update the quantity
        cart_item.quantity += int(quantity)
        cart_item.save()
    else:

        cart_item_d = Cart_items.objects.filter(
        user=request.user,cart__cart_items__cart_verify=False
        ).first()
        
        if cart_item_d:
    
            cart_item_instance = Cart_items.objects.filter(user=request.user, cart_verify=False).first()
            cart_item = Cart_items.objects.create(
                user=request.user, product=product, cart_id=cart_item_instance.cart_id, quantity=int(quantity)
            )
        else: 
            cart_id_d = Cart.objects.create(user=request.user)
            cart_item = Cart_items.objects.create(
                user=request.user, product=product, cart=cart_id_d, quantity=int(quantity)
            )


    return redirect('view_cart')

# def view_cart(request):
#     cart_items = Cart_items.objects.filter(user=request.user, cart_verify=False)

# #starting count code
#     user = request.user
#     user_cartd = Cart.objects.filter(user=user)
#     total_cart_items_count = 0
#     for user_cart in user_cartd:
#         cart_items_count = Cart_items.objects.filter(cart=user_cart, cart_verify=False).count()
#         total_cart_items_count += cart_items_count
# #ending count code

#     if not cart_items.exists():
#         # You can customize this part based on your requirements
#         empty_cart_message = "Your cart is empty."
#         categories = category.objects.all()
#         subcategories = sub_category.objects.all()
#         cart_items_count = 0  # Set count to 0 for an empty cart
#         context = {'empty_cart_message': empty_cart_message, 'cart_items_count': total_cart_items_count,
#                    'categories': categories, 'subcategories': subcategories}
#         return render(request, 'cart.html', context)
#     else: 
#     # Calculate the total amount in paise
#         total_amount_in_paise = sum(cart.product.current_price * 100 * cart.quantity for cart in cart_items)


#         categories = category.objects.all()
#         subcategories = sub_category.objects.all()
#         cart_items_count = Cart_items.objects.filter(user=request.user, cart_verify=True).count()

#         context = {'cart_items': cart_items, 'total_amount_in_paise': total_amount_in_paise,'cart_items_count': total_cart_items_count, 
#                                                     'categories': categories, 'subcategories': subcategories}
#         return render(request, 'cart.html', context)





def view_cart(request):
    cart_items = Cart_items.objects.filter(user=request.user, cart_verify=False)

    seller_coupons = {}

    for cart_item in cart_items:
     seller_id = cart_item.product.seller_id  # Assuming product has a foreign key to Seller
    #  if seller_id not in seller_coupons:
    #     # Fetch coupons associated with the seller and not expired
    #     coupons = Coupon.objects.filter(seller_id=seller_id, expiration_date__gte=timezone.now())
    #     seller_coupons[seller_id] = coupons
     if seller_id not in seller_coupons:
    # Fetch coupons associated with the seller and not expired
        coupons = Coupon.objects.filter(seller_id=seller_id, expiration_date__gte=timezone.now())
        
        # Get the list of coupon IDs already used by the user
        used_coupon_ids = CouponUsed.objects.filter(user=request.user).values_list('coupon_id', flat=True)
        
        # Filter out coupons that have already been used by the user
        filtered_coupons = [coupon for coupon in coupons if coupon.id not in used_coupon_ids]
        
        seller_coupons[seller_id] = filtered_coupons


#starting count code
    user = request.user
    user_cartd = Cart.objects.filter(user=user)
    total_cart_items_count = 0
    for user_cart in user_cartd:
        cart_items_count = Cart_items.objects.filter(cart=user_cart, cart_verify=False).count()
        total_cart_items_count += cart_items_count
#ending count code

    if not cart_items.exists():
        # You can customize this part based on your requirements
        empty_cart_message = "Your cart is empty."
        categories = category.objects.all()
        subcategories = sub_category.objects.all()
        cart_items_count = 0  # Set count to 0 for an empty cart
        context = {'empty_cart_message': empty_cart_message, 'cart_items_count': total_cart_items_count,
                   'categories': categories, 'subcategories': subcategories}
        return render(request, 'cart.html', context)
    else: 
    # Calculate the total amount in paise
        total_amount_in_paise = sum(cart.product.current_price * 100 * cart.quantity for cart in cart_items)


        categories = category.objects.all()
        subcategories = sub_category.objects.all()
        cart_items_count = Cart_items.objects.filter(user=request.user, cart_verify=True).count()

        context = {'cart_items': cart_items, 'total_amount_in_paise': total_amount_in_paise,'cart_items_count': total_cart_items_count, 
                                                    'categories': categories, 'subcategories': subcategories, 'seller_coupons': seller_coupons}
        return render(request, 'cart.html', context)





#delete cart item

def delete_cartitem(request, cart_id):
    cart_instance = get_object_or_404(Cart_items, id=cart_id)

    cart_instance.delete()

    return redirect('view_cart')

#view for wishlist
   
def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('product_not_found')

    cart_item = Wishlist.objects.create(user=request.user, product=product)

    cart_item.save()

    return redirect('view_wishlist')

#view wishlist item
@never_cache
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {'wishlist_items': wishlist_items}
    return render(request, 'wishlist.html', context)



#delet wishlist item

def delete_wishlistitem(request, item_id):
    wishlist_instance = get_object_or_404(Wishlist, id=item_id)

    if request.method == 'POST':
        wishlist_instance.delete()

    return redirect('view_wishlist')



def search_products(request):
    if request.method == 'GET' and 'search_term' in request.GET:
        search_term = request.GET['search_term']

        products = Product.objects.filter(
            Q(product_name__icontains=search_term) |
            Q(brand_name__icontains=search_term) |
            Q(category_id__category_name__icontains=search_term) |
            Q(sub_category_id__sub_category_name__icontains=search_term)
        )

        return render(request, 'search_results.html', {'products': products, 'search_term': search_term})
    return render(request, 'search.html')

def autocomplete_search(request):
    if 'term' in request.GET:
        search_term = request.GET['term']
        # Fetch suggestions based on product names, brand names, categories, and subcategories
        products = Product.objects.filter(
            ( Q(category_id__category_name__icontains=search_term)  | Q(brand_name__icontains=search_term)) |
            ( Q(product_name__icontains=search_term)|
             Q(sub_category_id__sub_category_name__icontains=search_term))
        ).values_list('product_name', 'brand_name', 'category_id__category_name', 'sub_category_id__sub_category_name')

        suggestions = list(set([item for sublist in products for item in sublist]))
        # Limit the suggestions to 5 results
        limited_suggestions = suggestions[:10]
        return JsonResponse(limited_suggestions, safe=False)
    return JsonResponse([], safe=False)



def update_cart_item_quantity(request, cart_item_id, new_quantity, currentPrice):
    cart_item = get_object_or_404(Cart_items, id=cart_item_id)
    
    # Check if the new quantity is valid (positive integer)
    try:
        new_quantity = int(new_quantity)
        if new_quantity <= 0:
            return JsonResponse({'error': 'Invalid quantity'})
    except ValueError:
        return JsonResponse({'error': 'Invalid quantity'})


    #return JsonResponse({"value data ": currentPrice})
    # Update the quantity
    cart_item.quantity = new_quantity
    cart_item.price = currentPrice
    cart_item.save()

    # You can return a success message or updated data if needed
    return JsonResponse({'success': 'Quantity updated successfully'})


#Checkout View
# def checkout_view(request):

#     try:
#         request.user.profile
#     except Profile.DoesNotExist:
#         # Redirect to a page indicating that the user profile is missing
#         return redirect('updateprofile') 
    
#     items_json = request.GET.get('items', '[]')
#     items = json.loads(items_json)

#     # Calculate total price
#     total_price = sum(item['quantity'] * item['price'] for item in items)

#     # Perform other checkout logic as needed
#     # ...
    
#     # Return JSON response with total price
#     response_data = {
#         'total_price': total_price,
#         'message': 'Checkout successful!',  # You can customize this message
#     }

#     return JsonResponse(response_data)

# def checkout_view(request):

#     items_json = request.GET.get('items', '[]')
#     items = json.loads(items_json)

#         # Calculate total price
#     total_price = sum(item['price'] for item in items)

#     try:
#         profile = request.user.profile
#         building_name = profile.building_name
#         road_area = profile.road_area
#         city = profile.city
#         state = profile.state
#         pincode = profile.pincode

#         context = {
#         'building_name': building_name,
#         'road_area': road_area,
#         'city': city,
#         'state': state,
#         'pincode': pincode,
#         'total_price': total_price,
#         }

#         return render(request, 'checkout.html', context)
#     except Profile.DoesNotExist:
#         context = {
#         'total_price': total_price,
#         }
         
#         return render(request, 'checkout.html', context)

    # Render the checkout template with address components and total_price


     
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



# @login_required
# def checkout_view(request):
#     # Get items from the request
#     items_json = request.GET.get('items', '[]')
#     items = json.loads(items_json)



#     for item in items:
#         item_id = item.get('item_id')
#         quantity = item.get('quantity')
#         price = item.get('price')

#         # Get the Cart_items instance
#         cart_item = get_object_or_404(Cart_items, id=item_id) 



#         # Update quantity and price
#         cart_item.quantity = quantity
#         cart_item.price = price
#         cart_item.cart_verify = 1
#         cart_item.save()
#         cart_itemd = get_object_or_404(Cart_items, id=item_id)
#         sessiondata = cart_itemd.cart_id

#     # Retrieve the cart_id from the Cart_items instance
#         request.session['cart_id'] = sessiondata 

#     # Calculate total price
#     total_price = sum(item['price'] for item in items)

#     try:
#         # Get user profile details
#         profile = request.user.profile
#         building_name = profile.building_name
#         road_area = profile.road_area
#         city = profile.city
#         state = profile.state
#         pincode = profile.pincode

#         currency = "INR"

#         request.session['amount'] = total_price
    
#         DATA = {
#         "amount": total_price * 100,
#         "currency": "INR",
#         "receipt": "receipt#2",
#         "notes": {
#             "key1": "value3",
#             "key2": "value2"
#         }
#         }
#         # Create a Razorpay Order
#         razorpay_order = razorpay_client.order.create(data=DATA)
    
#         # order id of newly created order.
#         razorpay_order_id = razorpay_order['id']
#         callback_url = '/myauth/paymenthandler/'
    
#         context = {}
#         context['razorpay_order_id'] = "orderhfgrhyfgjrgf"
#         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         context['razorpay_amount'] = total_price
#         context['currency'] = currency
#         context['callback_url'] = callback_url

#         context = {
#             'building_name': building_name,
#             'road_area': road_area,
#             'city': city,
#             'state': state,
#             'pincode': pincode,
#             'total_price': total_price,
#             'currency': currency,
#             'amount': total_price * 100,
#             'key': settings.RAZOR_KEY_ID,
#             'callback_url': callback_url,
#             'razorpay_order_id': razorpay_order_id
            
#         }

#         return render(request, 'checkout.html', context)
#     except Profile.DoesNotExist:
#         context = {
#             'total_price': total_price * 100,
#         }

#         return render(request, 'checkout.html', context)
    




@login_required
def checkout_view(request):
    # Get items from the request
    items_json = request.GET.get('items', '[]')
    discountdata = request.GET.get('discountdata','')
    cpid = request.GET.get('cpid', '')
    request.session['cpid_data_session'] = request.GET.get('cpid', '')
    request.session['cpid'] = cpid
    request.session['items'] = items_json
    request.session['discountdata'] = discountdata
   
    items = json.loads(items_json)


    seller_coupons = {}

    for item in items:
        item_id = item.get('item_id')
        quantity = item.get('quantity')
        price = item.get('price')
        seller_id = item.get('seller_id')

        # Get the Cart_items instance
        cart_item = get_object_or_404(Cart_items, id=item_id) 

        if seller_id:
            if seller_id not in seller_coupons:
                # Fetch coupons associated with the seller and not expired
                coupons = Coupon.objects.filter(seller_id=seller_id, expiration_date__gte=timezone.now())
                seller_coupons[seller_id] = coupons







        # Update quantity and price
        cart_item.quantity = quantity
        cart_item.price = price
        cart_item.cart_verify = 1
        cart_item.save()
        cart_itemd = get_object_or_404(Cart_items, id=item_id)
        sessiondata = cart_itemd.cart_id

    # Retrieve the cart_id from the Cart_items instance
        request.session['cart_id'] = sessiondata 

    # Calculate total price
    total_price = sum(item['price'] for item in items)

    

    if not discountdata:
      total_price_after_discount = total_price
    else:
      discount_multiplier = (100 - int(discountdata) ) / 100
      total_price_after_discount = total_price * discount_multiplier

# Reduce total price by the discount percentage
  #  total_price_after_discount = total_price * discount_multiplier

    try:
        # Get user profile details
        profile = request.user.profile
        building_name = profile.building_name
        road_area = profile.road_area
        city = profile.city
        state = profile.state
        pincode = profile.pincode

        currency = "INR"

        request.session['amount'] = total_price
    
        DATA = {
        "amount": int(total_price_after_discount) *100,
        "currency": "INR",
        "receipt": "receipt#2",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
        }
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(data=DATA)
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/myauth/paymenthandler/'
    
        context = {}
        context['razorpay_order_id'] = "orderhfgrhyfgjrgf"
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = total_price
        context['currency'] = currency
        context['callback_url'] = callback_url

        context = {
            'building_name': building_name,
            'road_area': road_area,
            'city': city,
            'state': state,
            'pincode': pincode,
            'total_price': int(total_price_after_discount),
            'currency': currency,
            'amount': int(total_price_after_discount) *100,
            'key': settings.RAZOR_KEY_ID,
            'callback_url': callback_url,
            'razorpay_order_id': razorpay_order_id,
            'seller_coupons': seller_coupons
            
        }

        print(seller_coupons)

        return render(request, 'checkout.html', context)
    except Profile.DoesNotExist:
        context = {
            'total_price': total_price * 100,
        }

        return render(request, 'checkout.html', context)




# @login_required
# def checkout_view_wallet(request):
#     # Get items from the request
#     items_json = request.GET.get('items', '[]')
#     discountdata = request.GET.get('discountdata','')
#     cpid = request.GET.get('cpid', '')
#     request.session['cpid'] = cpid
   
#     items = json.loads(items_json)


#     seller_coupons = {}

#     for item in items:
#         item_id = item.get('item_id')
#         quantity = item.get('quantity')
#         price = item.get('price')
#         seller_id = item.get('seller_id')

#         # Get the Cart_items instance
#         cart_item = get_object_or_404(Cart_items, id=item_id) 

#         if seller_id:
#             if seller_id not in seller_coupons:
#                 # Fetch coupons associated with the seller and not expired
#                 coupons = Coupon.objects.filter(seller_id=seller_id, expiration_date__gte=timezone.now())
#                 seller_coupons[seller_id] = coupons

#         # Update quantity and price
#         cart_item.quantity = quantity
#         cart_item.price = price
#         cart_item.cart_verify = 1
#         cart_item.save()
#         cart_itemd = get_object_or_404(Cart_items, id=item_id)
#         sessiondata = cart_itemd.cart_id

#     # Retrieve the cart_id from the Cart_items instance
#         request.session['cart_id'] = sessiondata 

#     # Calculate total price
#     total_price = sum(item['price'] for item in items)

    

#     if not discountdata:
#       total_price_after_discount = total_price
#     else:
#       discount_multiplier = (100 - int(discountdata) ) / 100
#       total_price_after_discount = total_price * discount_multiplier

# # Reduce total price by the discount percentage
#   #  total_price_after_discount = total_price * discount_multiplier

#     try:
#         # Get user profile details
#         profile = request.user.profile
#         building_name = profile.building_name
#         road_area = profile.road_area
#         city = profile.city
#         state = profile.state
#         pincode = profile.pincode

#         currency = "INR"

#         request.session['amount'] = total_price_after_discount

#         try:
#             current_datetime = timezone.now()
#             user_payment_instance = user_payment.objects.create(
#             user=request.user,
#             cart=request.session.get('cart_id'),
#             amount=request.session.get('amount'),
#             datetime=current_datetime,
#             order_id_data="nill",
#             payment_id_data="nill"
            
# )
            
#             cart = get_object_or_404(Cart, id=request.session.get('cart_id'))

#             # Retrieve all cart items for the given cart
#             cart_items = Cart_items.objects.filter(cart=cart)

#             # Update stock for each product based on the quantity ordered
#             for cart_item in cart_items:
#                 product = cart_item.product
#                 ordered_quantity = cart_item.quantity

#                 # Check if the ordered quantity is less than or equal to the available stock
#                 if ordered_quantity <= product.stock:
#                 # Update the stock
#                     product.stock -= ordered_quantity
#                     product.save()

#                     if product.stock <= 2:
#                         # Send email to the seller
#                         seller_email = product.seller_id.email
#                         subject = 'Low Stock Alert'
#                         message = f'Your product {product.product_name} is running low on stock. Current stock: {product.stock}'
#                         sender_email = settings.EMAIL_HOST_USER
#                         send_mail(subject, message, sender_email, [seller_email])

#             # capture the payment
#             # razorpay_client.payment.capture(payment_id, 321)
#             # render success page on successful capture of payment
#             if 'cpid' in request.session and request.session['cpid']:
#                 cpid = request.session['cpid']

#                 coupon_id = int(cpid)  # Extract the ID of the Coupon object
#                 user = request.user  # Assuming you have authenticated users
#                 coupon = get_object_or_404(Coupon, pk=coupon_id)
#                 coupon_used = CouponUsed.objects.create(user=user, coupon_id=coupon)
#                 # Optionally, you can clear the 'cpid' from the session after use
#                 request.session.pop('cpid')

#                 #do the coding here 
                
#             order_instance = Order.objects.create(
#             userpayment=user_payment_instance)
            
#             pincode = request.user.profile.pincode  # Assuming Profile is associated with User
#             delivery_boy_profile = Profile.objects.filter(pincode=pincode).first()

#             if delivery_boy_profile:
#                 delivery_boy = DeliveryBoy.objects.filter(pincode=pincode).first()
#             if delivery_boy:
#                 # Create DeliveryAssignment instance.
#                 delivery_assignment = DeliveryAssignment.objects.create(
#                     user=request.user,
#                     delivery_boy=delivery_boy,
#                     order=order_instance,
#                     assigned_at=current_datetime,
#                     status='PENDING'
#                 )


#             return redirect('payment_success')
#         except Exception as capture_error:
#             # if there is an error while capturing payment.
#             return JsonResponse({'error': str(capture_error)}, status=500)
#     except Profile.DoesNotExist:
#         context = {
#             'total_price': total_price * 100,
#         }

#         return render(request, 'checkout.html', context)


@login_required
def checkout_view_wallet(request):
    try:
        # Get the wallet object for the current user
        wallet = Wallet.objects.get(user=request.user)


        print(wallet.balance)

        # Get items from the request
        #items_json = request.GET.get('items', '[]')
        items_json = request.session.get('items')
        discountdata = str(request.session.get('discountdata', ''))

        cpid = request.session['cpid_data_session']
        request.session['cpid'] = cpid

        items = json.loads(items_json)

        seller_coupons = {}

        for item in items:
            item_id = item.get('item_id')
            quantity = item.get('quantity')
            price = item.get('price')
            seller_id = item.get('seller_id')

            # Get the Cart_items instance
            cart_item = get_object_or_404(Cart_items, id=item_id)

            if seller_id:
                if seller_id not in seller_coupons:
                    # Fetch coupons associated with the seller and not expired
                    coupons = Coupon.objects.filter(seller_id=seller_id, expiration_date__gte=timezone.now())
                    seller_coupons[seller_id] = coupons

            # Update quantity and price
            cart_item.quantity = quantity
            cart_item.price = price
            cart_item.cart_verify = 1
            cart_item.save()
            cart_itemd = get_object_or_404(Cart_items, id=item_id)
            sessiondata = cart_itemd.cart_id

            # Retrieve the cart_id from the Cart_items instance
            request.session['cart_id'] = sessiondata

        # Calculate total price
        total_price = sum(item['price'] for item in items)

        # Check if the wallet balance is sufficient
        if wallet.balance >= int(total_price):
            print("ggggggggggggggggggggggggggggggggggggggggg")
            if not discountdata:
                total_price_after_discount = total_price

            else:
                discount_multiplier = (100 - int(discountdata)) / 100
                total_price_after_discount = total_price * discount_multiplier

            # Deduct the total price from the wallet balance




            try:
                
                wallet.balance = wallet.balance -  int(total_price_after_discount)
                wallet.save()

                current_datetime = timezone.now()
                user_payment_instance = user_payment.objects.create(
                    user=request.user,
                    cart=request.session.get('cart_id'),
                    amount=request.session.get('amount'),
                    datetime=current_datetime,
                    order_id_data="nill",
                    payment_id_data="nill"
                )

                cart = get_object_or_404(Cart, id=request.session.get('cart_id'))

                # Retrieve all cart items for the given cart
                cart_items = Cart_items.objects.filter(cart=cart)

                # Update stock for each product based on the quantity ordered
                for cart_item in cart_items:
                    product = cart_item.product
                    ordered_quantity = cart_item.quantity

                    # Check if the ordered quantity is less than or equal to the available stock
                    if ordered_quantity <= product.stock:
                        # Update the stock
                        product.stock -= ordered_quantity
                        product.save()

                        if product.stock <= 2:
                            # Send email to the seller
                            seller_email = product.seller_id.email
                            subject = 'Low Stock Alert'
                            message = f'Your product {product.product_name} is running low on stock. Current stock: {product.stock}'
                            sender_email = settings.EMAIL_HOST_USER
                            send_mail(subject, message, sender_email, [seller_email])

                if 'cpid' in request.session and request.session['cpid']:
                    cpid = request.session['cpid']

                    coupon_id = int(cpid)  # Extract the ID of the Coupon object
                    user = request.user  # Assuming you have authenticated users
                    coupon = get_object_or_404(Coupon, pk=coupon_id)
                    coupon_used = CouponUsed.objects.create(user=user, coupon_id=coupon)
                    # Optionally, you can clear the 'cpid' from the session after use
                    request.session.pop('cpid')

                    # Do the coding here

                order_instance = Order.objects.create(
                    userpayment=user_payment_instance)

                pincode = request.user.profile.pincode  # Assuming Profile is associated with User
                delivery_boy_profile = Profile.objects.filter(pincode=pincode).first()

                if delivery_boy_profile:
                    delivery_boy = DeliveryBoy.objects.filter(pincode=pincode).first()
                if delivery_boy:
                    # Create DeliveryAssignment instance.
                    delivery_assignment = DeliveryAssignment.objects.create(
                        user=request.user,
                        delivery_boy=delivery_boy,
                        order=order_instance,
                        assigned_at=current_datetime,
                        status='PENDING'
                    )

                return redirect('payment_success')
            except Exception as capture_error:
                # If there is an error while capturing payment.
                return JsonResponse({'error': str(capture_error)}, status=500)
        else:
            # If the wallet balance is insufficient, redirect to the payment failed page
            return redirect('payment_failed')

    except Profile.DoesNotExist:
        context = {
            'total_price': total_price * 100,
        }

        return render(request, 'checkout.html', context)


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # return JsonResponse(params_dict)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            
            if result is not None:
                try:
                    current_datetime = timezone.now()
                    user_payment_instance = user_payment.objects.create(
                    user=request.user,
                    cart=request.session.get('cart_id'),
                    amount=request.session.get('amount'),
                    datetime=current_datetime,
                    order_id_data=razorpay_order_id,
                    payment_id_data=payment_id
                    
        )
                    
                    cart = get_object_or_404(Cart, id=request.session.get('cart_id'))

                    # Retrieve all cart items for the given cart
                    cart_items = Cart_items.objects.filter(cart=cart)

                    # Update stock for each product based on the quantity ordered
                    for cart_item in cart_items:
                        product = cart_item.product
                        ordered_quantity = cart_item.quantity

                        # Check if the ordered quantity is less than or equal to the available stock
                        if ordered_quantity <= product.stock:
                        # Update the stock
                            product.stock -= ordered_quantity
                            product.save()

                            if product.stock <= 2:
                                # Send email to the seller
                                seller_email = product.seller_id.email
                                subject = 'Low Stock Alert'
                                message = f'Your product {product.product_name} is running low on stock. Current stock: {product.stock}'
                                sender_email = settings.EMAIL_HOST_USER
                                send_mail(subject, message, sender_email, [seller_email])

                    # capture the payment
                    # razorpay_client.payment.capture(payment_id, 321)
                    # render success page on successful capture of payment
                    if 'cpid' in request.session and request.session['cpid']:
                        cpid = request.session['cpid']

                        coupon_id = int(cpid)  # Extract the ID of the Coupon object
                        user = request.user  # Assuming you have authenticated users
                        coupon = get_object_or_404(Coupon, pk=coupon_id)
                        coupon_used = CouponUsed.objects.create(user=user, coupon_id=coupon)
                        # Optionally, you can clear the 'cpid' from the session after use
                        request.session.pop('cpid')

                        #do the coding here 







                        
                    order_instance = Order.objects.create(
                    userpayment=user_payment_instance)
                    
                    pincode = request.user.profile.pincode  # Assuming Profile is associated with User
                    delivery_boy_profile = Profile.objects.filter(pincode=pincode).first()

                    if delivery_boy_profile:
                        delivery_boy = DeliveryBoy.objects.filter(pincode=pincode).first()
                    if delivery_boy:
                        # Create DeliveryAssignment instance.
                        delivery_assignment = DeliveryAssignment.objects.create(
                            user=request.user,
                            delivery_boy=delivery_boy,
                            order=order_instance,
                            assigned_at=current_datetime,
                            status='PENDING'
                        )

                    return redirect('payment_success')
                except Exception as capture_error:
                    # if there is an error while capturing payment.
                    return JsonResponse({'error': str(capture_error)}, status=500)
            else:
                # if signature verification fails.
                return JsonResponse({'error': 'Signature verification failed'}, status=400)
        except Exception as e:
            # if there is any other exception
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # if other than POST request is made.
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)
    






# from myauth.utils import send_whatsapp_message  # Assuming you have a function to send WhatsApp messages

# @csrf_exempt
# def paymenthandler(request):
#     if request.method == "POST":
#         try:
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')

#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             result = razorpay_client.utility.verify_payment_signature(params_dict)
            
#             if result is not None:
#                 try:
#                     current_datetime = timezone.now()
#                     user_payment_instance = user_payment.objects.create(
#                         user=request.user,
#                         cart=request.session.get('cart_id'),
#                         amount=request.session.get('amount'),
#                         datetime=current_datetime,
#                         order_id_data=razorpay_order_id,
#                         payment_id_data=payment_id
#                     )
                    
#                     cart = get_object_or_404(Cart, id=request.session.get('cart_id'))
#                     cart_items = Cart_items.objects.filter(cart=cart)

#                     for cart_item in cart_items:
#                         product = cart_item.product
#                         ordered_quantity = cart_item.quantity

#                         if ordered_quantity <= product.stock:
#                             product.stock -= ordered_quantity
#                             product.save()

#                             if product.stock <= 2:
#                                 # Send WhatsApp message to the seller
#                                 seller_phone_number = product.seller_id.sellerprofile.phone
#                                 message = f'Your product {product.product_name} is running low on stock. Current stock: {product.stock}'
#                                 send_whatsapp_message(seller_phone_number, message)

#                     return redirect('payment_success')
#                 except Exception as capture_error:
#                     return JsonResponse({'error': str(capture_error)}, status=500)
#             else:
#                 return JsonResponse({'error': 'Signature verification failed'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)
def payment_success(request):
    return render(request,'payment_success.html')



def payment_history(request):
    user = request.user

    # Get the cart items purchased by the user
    purchased_cart_items = Cart_items.objects.filter(
        cart__in=Subquery(
            user_payment.objects.filter(user=user).values('cart')
        )
    )

    context = {
        'purchased_cart_items': purchased_cart_items,
    }

    return render(request, 'history.html', context)

def list_reviews(request):
    # Get all product reviews
    reviews = product_review.objects.all()

    # Prepare data to be displayed
    review_data = []
    for review in reviews:
        print(review.product_id)
        product = Product.objects.get(id=review.product_id)
        review_data.append({
            'product_name': product.product_name,
            'product_image': product.image_1,
            'rating': review.product_rating,
            'description': review.description
        })

    context = {
        'reviews': review_data
    }
    return render(request, 'review.html', context)
def reviews(request):
    return render(request,'review.html')






def product_review_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_name_d = product.product_name  # Fetching the product name
    

    return render(request, 'product_review.html', {'product_name': product_name_d,'product_id' : product_id})


@login_required
def submit_review(request):
    if request.method == 'POST':
        product_rating = request.POST.get('product_rating')
        description = request.POST.get('description')
        product_id = request.POST.get('product_id')

        # Get the current user
        user = request.user

        # Get the current time using Django's timezone
        current_time = timezone.now()

        formatted_time = current_time.strftime('%d-%m-%Y %I:%M:%S %p')

        # Create a new product_review instance and save it to the database
        review = product_review.objects.create(
            user=user,
            product_id=product_id,
            created_at=formatted_time,
            product_rating=product_rating,
            description=description
        )

        return render(request,'review_success.html')  # Redirect to a success page

    # Render the form for GET requests
    return render(request, 'history.html')


#ALL product  view index
def productallview_index(request):
    items = Product.objects.all()
    categories = category.objects.all()
    subcategories = sub_category.objects.all()
    


    
    return render(request,'product_view_index.html',{'items': items , 
                                                 'categories': categories, 'subcategories': subcategories})





def productscategorylist_index(request, category_id):
    items = Product.objects.filter(category_id=category_id)
    # subcategories = sub_category.objects.filter(category_id=category_id)

    categories = category.objects.all()
    subcategories = sub_category.objects.all()
    
    return render(request, 'product_by_category.html', {'items': items,  
                                                 'categories': categories, 'subcategories': subcategories})


#deliveryboy_registration

def deliveryboy_registration(request):
    return render(request,'delivery_boy_registration.html')
    


#purchase history
@login_required
def purchasing_history(request):
    purchasing_history = user_payment.objects.select_related('user').all()
    return render(request, 'purchasing_history.html', {'purchasing_history': purchasing_history})

@login_required
def purchasing_histor(request):
    return render(request,'purchasing_history.html')

@login_required
def product_purchase_details(request):
    
    return render(request,'product_buy_details.html')

@login_required
def product_cart_details(request, cart_id):


    # Retrieve product details and related cart items for the specific cart_id
    cart_items = Cart_items.objects.select_related('product').filter(cart_id=cart_id)

    # Pass the cart_items to the template context
    context = {
        'cart_items': cart_items,
    }

    

    return render(request, 'product_buy_details.html', context)



#delivery boy 
def delivery_add_excel(request):
    return render(request,'delivery_boy_excel.html')   


#delivery boy registration 
# from django.core.mail import EmailMessage

# def sendmail_in_thread(subject, html_message, to_email):
#     email = EmailMessage(subject, html_message, to=to_email)
#     email.content_subtype = "html"
#     email.send()
# import pandas as pd

# def add_delivery_boys(request):
#     if request.method == 'POST' and 'xl_sheet' in request.FILES:
#         xl_sheet = request.FILES['xl_sheet']


#         try:
#             df = pd.read_excel(xl_sheet)

#             success_message_displayed = False  # Flag to track if success message has been displayed

#             for _, row in df.iterrows():
#                 # Create a unique username and password for each delivery boy
#                 username = row['Email']
#                 password = User.objects.make_random_password()

#                 user = User.objects.create_user(
#                     username=username,
#                     email=row['Email'],
#                     password=password,
#                     first_name=row['Firstname'],
#                     last_name=row['Lastname'],
#                     role='DELIVERYBOY'
#                 )

#                 contact_number = row['Contact Number']
#                 address = row['Address']
#                 vehicle_type = row['Vehicle Type']
#                 registration_number = row['Registration Number']
#                 delivery_zones = row['Delivery Zones']
#                 availability_timings = row['Availability Timings']

#                 delivery_boy = DeliveryBoy.objects.create(
#                     user=user,
#                     contact_number=contact_number,
#                     address=address,
#                     vehicle_type=vehicle_type,
#                     registration_number=registration_number,
#                     delivery_zones=delivery_zones,
#                     availability_timings=availability_timings
#                 )

#                 if not success_message_displayed:
#                     # Send an email to the delivery boy with their password
#                     subject = 'Welcome to the Delivery Service'
#                     html_message = render_to_string('email_to_deliveryboy.html', {
#                         'firstname': row['Firstname'],
#                         'password': password,
#                     })
#                     to_email = [row['Email']]

#                     # Use a thread to send the email asynchronously
#                     email_thread = threading.Thread(target=sendmail_in_thread, args=(subject, html_message, to_email))
#                     email_thread.start()

#                     # Notify the user that delivery boys were added successfully
#                     messages.success(request, 'Delivery boys added successfully.')
#                     success_message_displayed = True  # Update flag to indicate success message has been displayed

#         except Exception as e:
#             messages.error(request, f'Error processing the Excel sheet: {e}')

#     return render(request, 'delivery_boy_excel.html')


from django.core.mail import EmailMessage

def sendmail_in_thread(subject, html_message, to_email):
    email = EmailMessage(subject, html_message, to=to_email)
    email.content_subtype = "html"
    email.send()
import pandas as pd

def add_delivery_boys(request):
    if request.method == 'POST' and 'xl_sheet' in request.FILES:
        xl_sheet = request.FILES['xl_sheet']

        try:
            df = pd.read_excel(xl_sheet)
            success_message_displayed = False  # Flag to track if success message has been displayed

            for _, row in df.iterrows():
                username = row['Email']
                password = User.objects.make_random_password()

                user = User.objects.create_user(
                    username=username,
                    email=row['Email'],
                    password=password,
                    first_name=row['Firstname'],
                    last_name=row['Lastname'],
                    role='DELIVERYBOY'
                )

                contact_number = row['Contact Number']
                address = row['Address']
                vehicle_type = row['Vehicle Type']
                registration_number = row['Registration Number']
                delivery_zones = row['Delivery Zones']
                availability_timings = row['Availability Timings']

                delivery_boy = DeliveryBoy.objects.create(
                    user=user,
                    contact_number=contact_number,
                    address=address,
                    vehicle_type=vehicle_type,
                    registration_number=registration_number,
                    delivery_zones=delivery_zones,
                    availability_timings=availability_timings,
                    city = row['City'] , # New field
                    state = row['State'],  # New field
                    pincode = row['Pincode']  # New field
                )

                # Send an email to each delivery boy with their password
                subject = 'Welcome to the Delivery Service'
                html_message = render_to_string('email_to_deliveryboy.html', {
                    'firstname': row['Firstname'],
                    'password': password,
                })
                to_email = [row['Email']]

                # Use a thread to send the email asynchronously
                email_thread = threading.Thread(target=sendmail_in_thread, args=(subject, html_message, to_email))
                email_thread.start()

            # Notify the user that delivery boys were added successfully
            messages.success(request, 'Delivery boys added successfully.')
        except Exception as e:
            messages.error(request, f'Error processing the Excel sheet: {e}')

    return render(request, 'delivery_boy_excel.html')









#count
# def dashboard(request):
#     # Get the count of each role
#     customer_count = User.objects.filter(role='CUSTOMER').count()
#     seller_count = User.objects.filter(role='SELLER').count()
#     delivery_boy_count = User.objects.filter(role='DELIVERYBOY').count()

#     # Pass the counts to the template context
#     context = {
#         'customer_count': customer_count,
#         'seller_count': seller_count,
#         'delivery_boy_count': delivery_boy_count,

#     }

#     # Render the template with the context
#     return render(request, 'admintemplate.html', context)

def dashboardd(request):
    # Get the count of each role
    customer_count = User.objects.filter(role='CUSTOMER').count()
    seller_count = User.objects.filter(role='SELLER').count()
    delivery_boy_count = User.objects.filter(role='DELIVERYBOY').count()

    # Get the last three users from the notifications table
    last_three_notifications = Notification.objects.order_by('-id')[:3]
    last_three_users = [{'username': notification.user.username, 'current_date': notification.current_date, 'name': f"{notification.user.first_name} {notification.user.last_name}"} for notification in last_three_notifications]

    # Pass the counts and last three users to the template context
    context = {
        'customer_count': customer_count,
        'seller_count': seller_count,
        'delivery_boy_count': delivery_boy_count,
        'last_three_users': last_three_users,
    }

    # Render the template with the context
    return render(request, 'admintemplate.html', context)

#product reviews details
def prod_detail_review(request, product_id):
    subcategory_id = request.GET.get('subcat_id')

    product = Product.objects.get(id=product_id)
    product_images = product.product_images_set.all()

    categories = category.objects.all()
    subcategories = sub_category.objects.all()

    similar_products = Product.objects.filter(sub_category_id=subcategory_id).exclude(id=product_id)[:6]

    reviews = product_review.objects.filter(product_id=product_id)

    review_details = []
    for review in reviews:
        user_name = None
        if review.user:
            user_name = review.user.first_name
        review_details.append({
            'review_text': review.description,
            'review_username': user_name,
            'review_rating': review.product_rating,
            'dateinfo': review.created_at
        })

    return render(request, 'product_revieww.html', {
        'product': product,
        'product_images': product_images,
        'similarproducts': similar_products,
        'reviews': review_details,
        'categories': categories,
        'subcategories': subcategories
    })
    #return render(request,'product_revieww.html')   






from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import DeliveryBoy
import threading

def sendmail_in_thread(subject, html_message, to_email):
    email = EmailMessage(subject, strip_tags(html_message), to=to_email)
    email.content_subtype = "html"
    email.send()

def register_delivery_boy(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_no')
        address = request.POST.get('address')
        vehicle_type = request.POST.get('vehicle_type')
        registration_number = request.POST.get('registration')
        delivery_zones = request.POST.get('delivery_zones')
        availability_timings = request.POST.get('availability_timings')
        city = request.POST.get('city')  # New field
        state = request.POST.get('state')  # New field
        pincode = request.POST.get('pincode')  # New field

        random_password = get_user_model().objects.make_random_password()

        try:
            # Attempt to create a new user
            user = get_user_model().objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=email,
                email=email,
                password=random_password,
                role=get_user_model().Role.DELIVERYBOY
            )

            # Create the delivery boy with the provided contact number
            delivery_boy = DeliveryBoy.objects.create(
                user=user,
                contact_number=contact_number,
                address=address,
                vehicle_type=vehicle_type,
                registration_number=registration_number,
                delivery_zones=delivery_zones,
                availability_timings=availability_timings,
                city=city,  # New field
                state=state,  # New field
                pincode=pincode  # New field
            )
            
            # Send email with the random password
            subject = 'Welcome to the Delivery Service'
            html_message = render_to_string('email_to_deliveryboy.html', {'user': user, 'password': random_password})
            to_email = [email]

            # Use a thread to send the email asynchronously
            email_thread = threading.Thread(target=sendmail_in_thread, args=(subject, html_message, to_email))
            email_thread.start()

            # Redirect to a success URL or page upon successful registration
            messages.success(request, 'Delivery boys added successfully.')

        except IntegrityError:
            # Handle any IntegrityError
            # For example, you can redirect the user to a different page or display an error message
            messages.error(request, 'Delivery boys could not be added.')

    # Render the registration page template
    return render(request, 'delivery_boy_registration.html')





#delivery login
# def delivery_login(request):
    
#    return render(request,'delivery_dashboard.html')
# @login_required
# def delivery_login(request):
#     # Check if the delivery boy has already updated their password
#     if request.user.deliveryboy.has_updated_password:
#         return render(request, 'delivery_dashboard.html')  # Assuming 'delivery_login.html' is your login page
#     else:
#         return redirect('delivery_password')


@login_required
def delivery_delivered(request):
    # Check if the delivery boy has already updated their password
    if request.user.deliveryboy.has_updated_password:
        # Assuming 'delivery_dashboard.html' is your template for delivery dashboard
        # Fetch DeliveryAssignment instances related to the current delivery boy
        delivery_assignments = DeliveryAssignment.objects.filter( delivery_boy=request.user.deliveryboy, status='DELIVERED' ).order_by('-assigned_at')

        # Get user details associated with each delivery assignment
        assignment_details = []
        for assignment in delivery_assignments:
            assignment_details.append({
                'assignment': assignment,
                "email": assignment.user.email,
                "name": assignment.user.first_name,
                "last": assignment.user.last_name,


                'user_details': assignment.user.profile  # Assuming profile is related to User through OneToOneField
            })

        # Pass the data to the template for rendering
        return render(request, 'delivery_dashboard.html', {'assignment_details': assignment_details})
    else:
        return redirect('delivery_password')  # Assuming 'delivery_password' is the name of the view where delivery boy updates password


@login_required
def delivery_login(request):
    # Check if the delivery boy has already updated their password
    if request.user.deliveryboy.has_updated_password:
        # Assuming 'delivery_dashboard.html' is your template for delivery dashboard
        # Fetch DeliveryAssignment instances related to the current delivery boy
        delivery_assignments = DeliveryAssignment.objects.filter( delivery_boy=request.user.deliveryboy ).exclude(status='DELIVERED').order_by('-assigned_at')

        # Get user details associated with each delivery assignment
        assignment_details = []
        for assignment in delivery_assignments:
            assignment_details.append({
                'assignment': assignment,
                "email": assignment.user.email,
                "name": assignment.user.first_name,
                "last": assignment.user.last_name,


                'user_details': assignment.user.profile  # Assuming profile is related to User through OneToOneField
            })

        # Pass the data to the template for rendering
        return render(request, 'delivery_dashboard.html', {'assignment_details': assignment_details})
    else:
        return redirect('delivery_password')  # Assuming 'delivery_password' is the name of the view where delivery boy updates password


@login_required
def update_delivery_status(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        status = request.POST.get('status')

        try:
            assignment = DeliveryAssignment.objects.get(id=assignment_id)
            assignment.status = status
            assignment.save()
            return redirect('delivery_login')
        except DeliveryAssignment.DoesNotExist:
            return HttpResponseBadRequest("Invalid Assignment ID")

    return HttpResponseBadRequest("Invalid Request")


def verify_otp_delivery(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        assignment_id = request.POST.get('out_for_delivery')

        # Retrieve the delivery assignment
        assignment = DeliveryAssignment.objects.get(id=assignment_id)

        # Retrieve the OTP from the database
        try:
            delivery_otp = DeliveryOTP.objects.get(assignment=assignment)
        except DeliveryOTP.DoesNotExist:
            return HttpResponse('OTP not found!')

        # Verify the OTP
        if otp == delivery_otp.otp:
            # Update delivery status to "DELIVERED"
            assignment.status = 'DELIVERED'
            assignment.save()

            # You can add more logic here if needed

            return redirect('delivery_login')
        else:
            return HttpResponse('Invalid OTP!')

    return HttpResponse('Invalid request method!')

from django.contrib.auth import update_session_auth_hash

@login_required
def Change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()

            # Update session to prevent the user from being logged out
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully.')
            return redirect('delivery_login')
        else:
            messages.error(request, 'Passwords do not match.')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delivery_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()

            # Update session to prevent the user from being logged out
            update_session_auth_hash(request, user)

            # Update the DeliveryBoy instance to mark that password is updated
            delivery_boy = DeliveryBoy.objects.get(user=user)
            delivery_boy.has_updated_password = True
            delivery_boy.save()

            messages.success(request, 'Password changed successfully.')
            return redirect('delivery_login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('delivery_password')  # Redirect back to the password change page if passwords don't match
    else:
        return render(request, 'delivery_password.html')




# from reportlab.pdfgen import canvas
# from .models import user_payment

# def generate_user_payment_pdf(request, user_id):
#     # Get the user object
#     user = User.objects.get(id=user_id)

#     # Get the user's payment objects
#     user_payments = user_payment.objects.filter(user=user)

#     # Create a PDF response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename="{user.username}_payment_history.pdf"'

#     # Create the PDF content
#     p = canvas.Canvas(response)
#     p.drawString(100, 800, f"Payment History for User: {user.username}")

#     # Add user payment details to the PDF
#     y_position = 780
#     for payment in user_payments:
#         p.drawString(100, y_position, f"Amount: Rs{payment.amount}")
#         p.drawString(100, y_position - 20, f"Date and Time: {payment.datetime}")
#         p.drawString(100, y_position - 40, f"Order ID Data: {payment.order_id_data}")
#         p.drawString(100, y_position - 60, f"Payment ID Data: {payment.payment_id_data}")
#         y_position -= 100  # Adjust vertical position for the next payment details
#         # Add more details as needed

#     # Save the PDF content
#     p.showPage()
#     p.save()

#     return response


#payment detailes pdf download

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from .models import user_payment

def generate_user_latest_payment_pdf(request, user_id):
    # Get the latest payment for the user
    latest_payment = user_payment.objects.filter(user_id=user_id).latest('datetime')

    # Create a PDF buffer
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'filename="{latest_payment.user.username}_latest_payment.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define data for the PDF
    data = [
        ["Amount", latest_payment.amount],
        ["Date and Time", latest_payment.datetime],
        ["Order ID Data", latest_payment.order_id_data],
        ["Payment ID Data", latest_payment.payment_id_data]
    ]

    # Create a table with data
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
    ]))

    # Add table to the PDF document
    doc.build([Paragraph(f" Payment Details for User: {latest_payment.user.username}", styles['Title']), table])

    return buffer 
    

    # views.py

# views.py

# views.py









#delivery boy view in admin dashboard
@login_required
def delivery_vieww(request):
    delivery_boys = DeliveryBoy.objects.all()
    return render(request,'deliveryboy_view.html', {'delivery_boys': delivery_boys})  




#deliveryboy view and activate and deactivate 
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def activate_delivery_boy(request, delivery_boy_id):
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    delivery_boy.user.is_active = True
    delivery_boy.user.save()

    # Send activation email
    send_mail(
        'Your account has been activated',
        'Dear {},\n\nYour account has been activated.'.format(delivery_boy.user.get_full_name()),
        'your_email@example.com',  # Set your email here
        [delivery_boy.user.email],
        fail_silently=False,
    )

    messages.success(request, f"{delivery_boy.user.get_full_name} has been activated.")
    return redirect('delivery_vieww')

def deactivate_delivery_boy(request, delivery_boy_id):
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    delivery_boy.user.is_active = False
    delivery_boy.user.save()

    # Send deactivation email
    send_mail(
        'Your account has been deactivated',
        'Dear {},\n\nYour account has been deactivated.'.format(delivery_boy.user.get_full_name()),
        'your_email@example.com',  # Set your email here
        [delivery_boy.user.email],
        fail_silently=False,
    )

    messages.success(request, f"{delivery_boy.user.get_full_name} has been deactivated.")
    return redirect('delivery_vieww')





def notification_view(request):
    # Retrieve all notifications from the database
    notifications = Notification.objects.all()

    # Pass the notifications to the template context
    context = {
        'notifications': notifications,
    }

    # Render the HTML template
    return render(request, 'notification_view.html', context)


#sellers item view

def sellers_item(request):
    # Retrieve all sellers
    sellers = User.objects.filter(role='SELLER')
    
    context = {
        'sellers': sellers,
    }
    
    return render(request, 'sellers_item.html', context)



def seller_products_view(request, seller_id):
    # Retrieve the seller based on the seller_id
    seller = User.objects.get(id=seller_id)

    # Retrieve products added by the seller
    seller_products = Product.objects.filter(seller_id=seller_id)

    context = {
        'seller': seller,
        'seller_products': seller_products,
    }

    return render(request, 'seller_products.html', context)







 # views.py

from django.shortcuts import render
from django.utils.crypto import get_random_string

import base64

# def generate_coupon(request):
#     if request.method == 'POST':
#         # Generate a random coupon code
#         coupon_code = get_random_string(length=8)
        
#         # Define the discount percentage
#         discount_percentage = 20  # Adjust as needed
        
#         # Generate the QR code containing the coupon details
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(f"Coupon Code: {coupon_code}\nDiscount Percentage: {discount_percentage}%")
#         qr.make(fit=True)
#         qr_img = qr.make_image(fill_color="black", back_color="white")

#         # Convert the QR code image to Base64 string
#         buffer = io.BytesIO()
#         qr_img.save(buffer, format='PNG')
#         qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

#         # Render the coupon template with the coupon code and discount percentage
#         return render(request, 'seller_dashboard.html', {'coupon_code': coupon_code, 'discount_percentage': discount_percentage, 'qr_code_base64': qr_image_base64})
#     else:
#         return render(request, 'seller_dashboard.html')





# views.py

# views.py

# from django.shortcuts import render
# from django.utils.crypto import get_random_string
# import qrcode
# from io import BytesIO
# from django.core.files.base import ContentFile
# from .models import Coupon
# import base64

# def generate_coupon(request):
#     if request.method == 'POST':
#         # Generate a random coupon code
#         coupon_code = get_random_string(length=8)
        
#         # Define the discount percentage
#         discount_percentage = 20  # Adjust as needed
        
#         # Generate the QR code containing the coupon details
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(f"Coupon Code: {coupon_code}\nDiscount Percentage: {discount_percentage}%")
#         qr.make(fit=True)
#         qr_img = qr.make_image(fill_color="black", back_color="white")

#         # Convert the QR code image to bytes
#         buffer = BytesIO()
#         qr_img.save(buffer, format='PNG')
#         qr_image_bytes = buffer.getvalue()

#         # Convert the QR code image bytes to base64
#         qr_image_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')

#         # Save the coupon details to the database
#         coupon = Coupon.objects.create(coupon_code=coupon_code, discount_percentage=discount_percentage)

#         # Render the coupon template with the coupon code, discount percentage, and QR code
#         return render(request, 'coupon.html', {'coupon': coupon, 'qr_code_base64': qr_image_base64})
#     else:
#         return render(request, 'coupon.html')


from django.shortcuts import render
from django.utils.crypto import get_random_string
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Coupon
import base64

# def generate_coupon(request):
#     if request.method == 'POST':
#         # Generate a random coupon code
#         coupon_code = get_random_string(length=8)
        
#         # Define the discount percentage
#         discount_percentage = 20  # Adjust as needed
        
#         # Generate the QR code containing the coupon details
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(f"Coupon Code: {coupon_code}\nDiscount Percentage: {discount_percentage}%")
#         qr.make(fit=True)
#         qr_img = qr.make_image(fill_color="black", back_color="white")

#         # Convert the QR code image to bytes
#         buffer = BytesIO()
#         qr_img.save(buffer, format='PNG')
#         qr_image_bytes = buffer.getvalue()

#         # Convert the QR code image bytes to base64
#         qr_image_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')

#         # Assuming you are using the built-in User model for authentication
#         seller_id_data = request.user  

#         # Save the coupon details to the database
#         coupon = Coupon.objects.create(
#             coupon_code=coupon_code,
#             discount_percentage=discount_percentage,
#             seller_id=seller_id_data,
#             expiration_date='2099-12-31'  # Manually defining default expiration date
#         )

#         # Render the coupon template with the coupon code, discount percentage, and QR code
#         return render(request, 'coupon.html', {'coupon': coupon, 'qr_code_base64': qr_image_base64})
#     else:
#         return render(request, 'generate_coupon.html')


def generate_coupon(request):
    if request.method == 'POST':
        # Retrieve form data
        selected_date = request.POST.get('selected_date')
        selected_percentage = request.POST.get('selected_percentage')

        # Generate a random coupon code
        coupon_code = get_random_string(length=8)
        
        # Convert the selected_percentage to an integer
        discount_percentage = int(selected_percentage)

        # Generate the QR code containing the coupon details
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"Coupon Code: {coupon_code}\nDiscount Percentage: {discount_percentage}%")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Convert the QR code image to bytes
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_image_bytes = buffer.getvalue()

        # Convert the QR code image bytes to base64
        qr_image_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')

        # Assuming you are using the built-in User model for authentication
        seller_id_data = request.user  

        # Save the coupon details to the database
        coupon = Coupon.objects.create(
            coupon_code=coupon_code,
            discount_percentage=discount_percentage,
            seller_id=seller_id_data,
            expiration_date=selected_date
        )

        # Render the coupon template with the coupon code, discount percentage, and QR code
        return render(request, 'coupon.html', {'coupon': coupon, 'qr_code_base64': qr_image_base64})
    else:
        # Render the form template
        return render(request, 'generate_coupon.html')






# views.py

# views.py

# views.py

# @login_required
# def list_purchased_users_of_seller(request):
#     if request.user.role == User.Role.SELLER:  # Check if the current user is a seller
#         purchased_users = User.objects.filter(cart_items__product__seller_id=request.user).distinct()
#         context = {
#             'purchased_users': purchased_users
#         }
#         return render(request, 'seller_products_purchase_users.html', context)
#     else:
#         # If the current user is not a seller, redirect or handle accordingly
#         # For example:
#         return render(request, 'error_page.html', {'error_message': 'You are not authorized to view this page.'})
    




@login_required
def list_purchased_users_of_seller(request):
    if request.user.role == User.Role.SELLER:  # Check if the current user is a seller
        purchased_users = User.objects.filter(cart_items__product__seller_id=request.user).distinct()
        context = {
            'purchased_users': purchased_users
        }
        return render(request, 'seller_products_purchase_users.html', context)
    else:
        # If the current user is not a seller, redirect or handle accordingly
        # For example:
        return render(request, 'error_page.html', {'error_message': 'You are not authorized to view this page.'})
    




def seller_product_user_view(request):
    return render(request,'seller_products_purchase_users.html')  


# def view_purchased_products(request, user_id):
#     if request.user.role == User.Role.SELLER:  # Check if the current user is a seller
#         user = User.objects.get(id=user_id)
#         purchased_products = Product.objects.filter(cart_items__user=user)
#         context = {
#             'user': user,
#             'purchased_products': purchased_products
#         }
#         return render(request, 'view_purchased_products.html', context)
#     else:
#         # Handle unauthorized access
#         return render(request, 'error_page.html', {'error_message': 'You are not authorized to view this page.'})
@login_required
def view_purchased_products(request, user_id):
    if request.user.role == User.Role.SELLER:  # Check if the current user is a seller
        user = User.objects.get(id=user_id)
        purchased_products = Product.objects.filter(cart_items__user=user)

        # Handling search functionality
        query = request.GET.get('q')
        if query:
            # Filter purchased products by product_name containing the query string
            purchased_products = purchased_products.filter(product_name__icontains=query)

        # Handling filter functionality
        # You can add more filter options as needed
        filters = {}
        category_name = request.GET.get('category')
        subcategory_name = request.GET.get('subcategory')
        brand_name = request.GET.get('brand')  # Added for brand filtering
        if category_name:
            # Filter purchased products by category name
            purchased_products = purchased_products.filter(category_id__category_name=category_name)
            filters['category'] = category_name
        if subcategory_name:
            # Filter purchased products by subcategory name
            purchased_products = purchased_products.filter(category_id__sub_category__sub_category_name=subcategory_name)
            filters['subcategory'] = subcategory_name
        if brand_name:
            # Filter purchased products by brand name
            purchased_products = purchased_products.filter(brand_name=brand_name)
            filters['brand'] = brand_name

        # Pass distinct category names, subcategory names, and brand names to the template for the dropdown menus
        distinct_categories = category.objects.values_list('category_name', flat=True).distinct()
        # distinct_subcategories = SubCategory.objects.values_list('sub_category_name', flat=True).distinct()
        distinct_brands = Product.objects.values_list('brand_name', flat=True).distinct()

        # Pass the filter options to the template
        context = {
            'user': user,
            'purchased_products': purchased_products,  
            'filters': filters,
            'distinct_categories': distinct_categories,
            # 'distinct_subcategories': distinct_subcategories,
            'distinct_brands': distinct_brands,
        }
        return render(request, 'view_purchased_products.html', context)
    else:
        # Handle unauthorized access
        return render(request, 'error_page.html', {'error_message': 'You are not authorized to view this page.'})


       

def coupon(request):
    return render(request,'coupon.html') 



# def coupon_list(request):
#     return render(request,'seller_coupon_list.html') 



from django.shortcuts import render
from .models import Coupon

def display_seller_coupons(request):
    # Assuming the user is logged in and is a seller
    user = request.user
    print(user)  


    
    # Retrieve coupons for the seller
    coupons = Coupon.objects.filter(seller_id=user.id, visibility=True)
    
    # Pass the coupons to the template for display
    return render(request, 'seller_coupon_list.html', {'coupons': coupons})



#seller view their product review
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product

@login_required
def seller_view_review(request):
    # Assuming the logged-in user is a seller
    seller = request.user

    # Filter products based on the seller_id field
    seller_products = Product.objects.filter(seller_id=seller)

    # Handling search functionality
    query = request.GET.get('q')
    if query:
        # Filter products by product_name containing the query string
        seller_products = seller_products.filter(product_name__icontains=query)

    # Handling filter functionality
    # You can add more filter options as needed
    filters = {}
    category_name = request.GET.get('category')
    subcategory_name = request.GET.get('subcategory')
    brand_name = request.GET.get('brand')
    if category_name:
        # Filter products by category name
        seller_products = seller_products.filter(category_id__category_name=category_name)
        filters['category'] = category_name
    if subcategory_name:
        # Filter products by subcategory name
        seller_products = seller_products.filter(sub_category_id__sub_category_name=subcategory_name)
        filters['subcategory'] = subcategory_name
    if brand_name:
        # Filter products by brand name
        seller_products = seller_products.filter(brand_name=brand_name)
        filters['brand'] = brand_name

    # Pass distinct category names and brand names to the template for the dropdown menus
    distinct_categories = category.objects.values_list('category_name', flat=True).distinct()
    distinct_brands = Product.objects.values_list('brand_name', flat=True).distinct()

    # Pass the filter options to the template
    context = {
        'seller_products': seller_products,
        'filters': filters,
        'distinct_categories': distinct_categories,
        'distinct_brands': distinct_brands,
    }

    return render(request, 'seller_view_product_reviews.html', context)




def seller_prod_detail_reviewsss(request, product_id):
    # Get the product corresponding to the product_id
    product = get_object_or_404(Product, id=product_id)

    # Retrieve product images related to the product
    product_images = product.product_images_set.all()

    # Retrieve all categories and subcategories for navigation
    categories = category.objects.all()
    subcategories = sub_category.objects.all()

    # Get similar products based on the subcategory of the current product
    similar_products = Product.objects.filter(sub_category_id=product.sub_category_id).exclude(id=product_id)[:6]

    # Retrieve reviews related to the product
    reviews = product_review.objects.filter(product_id=product_id)

    # Prepare review details to be passed to the template
    review_details = []
    for review in reviews:
        user_name = None
        if review.user:
            user_name = review.user.first_name
        review_details.append({
            'review_text': review.description,
            'review_username': user_name,
            'review_rating': review.product_rating,
            'dateinfo': review.created_at
        })

    return render(request, 'seller_view_product_reviewsss.html', {
        'product': product,
        'product_images': product_images,
        'similar_products': similar_products,
        'reviews': review_details,
        'categories': categories,
        'subcategories': subcategories
    })







#seller view their product review
#seller view their product review
def seller_view_notification(request):
    low_stock_products = Product.objects.filter(seller_id=request.user, stock__lte=2)
    
    context = {
        'low_stock_products': low_stock_products
    }
    
    return render(request, 'seller_notification.html', context)


from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def download_low_stock_products_pdf(request):
    low_stock_products = Product.objects.filter(seller_id=request.user, stock__lte=2)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="low_stock_products.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title = Paragraph('<b>Low Stock Products Report</b>', styles['Title'])
    elements.append(title)
    
    data = []
    data.append([Paragraph('<b>Product Name</b>', styles['Normal']),
                 Paragraph('<b>Brand</b>', styles['Normal']),
                 Paragraph('<b>Stock</b>', styles['Normal']),
                 Paragraph('<b>Product Number</b>', styles['Normal'])])
    
    for i, product in enumerate(low_stock_products):
        bg_color = colors.lightgrey if i % 2 == 0 else colors.white
        data.append([Paragraph(product.product_name, styles['Normal']),
                     Paragraph(product.brand_name, styles['Normal']),
                     str(product.stock),
                     product.product_number])
    
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), bg_color),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
    elements.append(table)
    
    doc.build(elements)
    return response









from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Coupon

# def delete_coupon(request, coupon_id):
#     # Retrieve the coupon object
#     coupon = get_object_or_404(Coupon, pk=coupon_id)

#     # Check if the coupon has already been used (visibility is False)
#     if not coupon.visibility:
#         # If the coupon has already been used, return JsonResponse indicating it cannot be deleted
#         return JsonResponse({'message': 'Coupon has already been used and cannot be deleted.'}, status=400)

#     # If the coupon has not been used, delete it from the database
#     coupon.delete()

#     # Return JsonResponse indicating successful deletion
#     return JsonResponse({'message': 'Coupon deleted successfully.'})



def delete_coupon(request, coupon_id):
    # Retrieve the coupon object
    coupon = get_object_or_404(Coupon, pk=coupon_id)

    # Check if the coupon has already been used (visibility is False)
    if not coupon.visibility:
        # If the coupon has already been used, return JsonResponse indicating it cannot be deleted
        return JsonResponse({'message': 'Coupon has already been used and cannot be deleted.'}, status=400)

    # If the coupon has not been used, delete it from the database
    coupon.delete()

    # Redirect the user to the specified URL after successful deletion
    return redirect('/myauth/coupon_list/')

# def delete_coupon(request, coupon_id):
#     # Retrieve the coupon object
#     coupon = get_object_or_404(Coupon, pk=coupon_id)

#     # Set the visibility of the coupon to False
#     coupon.visibility = False
#     coupon.save()

#     # Redirect the user to a specific URL after updating the visibility
#     return redirect('/myauth/coupon_list/')







def purchase_orders(request):
    # Fetch user_payments
    user_payments = user_payment.objects.all()
    
    # Create a list to store order details
    orders = []
    
    # Loop through user_payments to fetch related Cart_items and Product details
    for payment in user_payments:
        cart_items = Cart_items.objects.filter(user=payment.user, cart=payment.cart)
        for item in cart_items:
            orders.append({
                'user': payment.user,
                'address': payment.user.profile.building_name + ", " + payment.user.profile.road_area,
                'state': payment.user.profile.state,
                'district': payment.user.profile.city,
                'pincode': payment.user.profile.pincode,
                'product_name': item.product.product_name,
                'quantity': item.quantity,
                'price': item.price
            })
    
    context = {
        'orders': orders
    }
    return render(request, 'purchase_orders.html', context)



#seller virew purchase detail of their products


# from operator import itemgetter

# def purchase_detailsss(request):
#     # Assuming the logged-in user is a seller
#     seller = request.user

#     # Get all Cart_items associated with the seller's products
#     seller_cart_items = Cart_items.objects.filter(product__seller_id=seller)

#     # Create a list to store payment details, product name, username, and number of items for each seller's product
#     seller_details = []

#     # Iterate over each Cart_items object and fetch its associated payment details
#     for cart_item in seller_cart_items:
#         payment_details = user_payment.objects.filter(cart=cart_item.cart_id).first()
#         if payment_details:
#             # Fetch the username associated with the payment
#             username = payment_details.user.first_name
#             last_name = payment_details.user.last_name

#             # Append payment details, username, product name, and number of items to the list
#             seller_details.append({
#                 'payment_details': payment_details,
#                 'username': username,
#                 'last_name': last_name,
#                 'product_name': cart_item.product.product_name,
#                 'product_number': cart_item.product.product_number,
#                 'brand_name': cart_item.product.brand_name,
#                 'stock': cart_item.product.stock,
#                 'price': cart_item.product.current_price,
#                 'image_1': cart_item.product.image_1,  # Add the main image URL to the dictionary
#                 'num_items': cart_item.quantity
#             })

#     # Sort the seller_details list based on the order ID data of payment details
#     seller_details.sort(key=lambda x: x['payment_details'].order_id_data, reverse=True)

#     context = {
#         'seller_details': seller_details,
#     }

#     return render(request, 'purchase_details_by_seller_products.html', context)
from django.shortcuts import render
from .models import user_payment, Cart_items

def purchase_detailsss(request):
    # Assuming the logged-in user is a seller
    seller = request.user

    # Get all Cart_items associated with the seller's products
    seller_cart_items = Cart_items.objects.filter(product__seller_id=seller)

    # Filter by date range if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        # Correct the lookup to match the actual field name
        seller_cart_items = seller_cart_items.filter(payment__datetime__range=(start_date, end_date))

    # Filter by price range if provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        seller_cart_items = seller_cart_items.filter(product__current_price__range=(min_price, max_price))

    # Create a list to store payment details, product name, username, and number of items for each seller's product
    seller_details = []

    # Iterate over each Cart_items object and fetch its associated payment details
    for cart_item in seller_cart_items:
        payment_details = user_payment.objects.filter(cart=cart_item.cart_id).first()
        if payment_details:
            # Fetch the username associated with the payment
            username = payment_details.user.first_name
            last_name = payment_details.user.last_name

            # Append payment details, username, product name, and number of items to the list
            seller_details.append({
                'payment_details': payment_details,
                'username': username,
                'last_name': last_name,
                'product_name': cart_item.product.product_name,
                'product_number': cart_item.product.product_number,
                'brand_name': cart_item.product.brand_name,
                'stock': cart_item.product.stock,
                'price': cart_item.product.current_price,
                'image_1': cart_item.product.image_1,  # Add the main image URL to the dictionary
                'num_items': cart_item.quantity
            })

    # Sort the seller_details list based on the order ID data of payment details
    seller_details.sort(key=lambda x: x['payment_details'].order_id_data, reverse=True)

    context = {
        'seller_details': seller_details,
    }

    return render(request, 'purchase_details_by_seller_products.html', context)











@login_required
def seller_display_product(request):
    # Assuming the logged-in user is a seller
    seller = request.user

    # Filter products based on the seller_id field
    seller_products = Product.objects.filter(seller_id=seller)

    # Handling search functionality
    query = request.GET.get('q')
    if query:
        # Filter products by product_name containing the query string
        seller_products = seller_products.filter(product_name__icontains=query)

    # Handling filter functionality
    # You can add more filter options as needed
    filters = {}
    category_name = request.GET.get('category')
    subcategory_name = request.GET.get('subcategory')
    brand_name = request.GET.get('brand')
    if category_name:
        # Filter products by category name
        seller_products = seller_products.filter(category_id__category_name=category_name)
        filters['category'] = category_name
    if subcategory_name:
        # Filter products by subcategory name
        seller_products = seller_products.filter(sub_category_id__sub_category_name=subcategory_name)
        filters['subcategory'] = subcategory_name
    if brand_name:
        # Filter products by brand name
        seller_products = seller_products.filter(brand_name=brand_name)
        filters['brand'] = brand_name

    # Pass distinct category names and brand names to the template for the dropdown menus
    distinct_categories = category.objects.values_list('category_name', flat=True).distinct()
    distinct_brands = Product.objects.values_list('brand_name', flat=True).distinct()

    # Pass the filter options to the template
    context = {
        'seller_products': seller_products,
        'filters': filters,
        'distinct_categories': distinct_categories,
        'distinct_brands': distinct_brands,
    }

    return render(request, 'seller_products_product_view.html', context)



def new_orders(request):
    if request.user.is_authenticated and hasattr(request.user, 'deliveryboy'):
        delivery_boy = request.user.deliveryboy
        orders = DeliveryAssignment.objects.filter(delivery_boy=delivery_boy, status='PENDING')
        addresses = {}
        for assignment in orders:
            # Retrieve the address associated with the user in the delivery assignment
            address = Address.objects.filter(user=assignment.user).first()
            if address:
                addresses[assignment.id] = address

        context = {
            'pending_assignments': orders,
            'addresses': addresses,
        }

        return render(request, 'Delivery/new_orders.html', context)
    else:
        # Redirect or handle the case where the user is not authenticated or not a delivery boy
        return render(request, 'error_page.html', {'message': 'Unauthorized access'})
    










# def trackmyorder(request):
#     user=request.user
#     order=DeliveryAssignment.objects.filter(user=user)
#     context={
#         'order':order
#     }
#     return render (request,'trackmyorder.html',context)


def trackmyorder(request):
    user = request.user
    orders = DeliveryAssignment.objects.filter(user=user).exclude(status="DELIVERED")
    orders_with_cart_id = []
    
    for order in orders:
        # Fetch the related user_payment object for the order
        user_payment_obj = user_payment.objects.filter(user=user, order=order.order).first()
        cart_id = None
        if user_payment_obj:
            cart_id = user_payment_obj.cart
        order_dict = {
            'order': order,
            'cart_id': cart_id
        }
        orders_with_cart_id.append(order_dict)
    
    context = {
        'orders_info': orders_with_cart_id
    }
    return render(request, 'trackmyorder.html', context)



def view_products_user(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        if cart_id:
            # Fetch cart items based on the cart_id
            cart_items = Cart_items.objects.filter(cart_id=cart_id)
            # Get products associated with cart items
            products = [item.product for item in cart_items]
            context = {'products': products}
            return render(request, 'view_products_user.html', context)
    # Handle cases where cart_id is not provided or POST method is not used
    return render(request, 'error.html', {'message': 'Invalid request'})


def create_otp(request):
    if request.method == 'POST':
        out_for_delivery = request.POST.get('out_for_delivery')
        email = request.POST.get('email')

        # Generate OTP
        otp = ''.join(random.choices(string.digits, k=6))

        # Send email with OTP
        send_mail(
            'Your OTP for Delivery',
            f'Your OTP for the delivery is: {otp}',
            'prxnv2832@gmail.com',  # Replace with your sender email
            [email],
            fail_silently=False,
        )

        # Save OTP to database
        otp_instance = DeliveryOTP.objects.create(
            otp=otp,
            assignment_id=out_for_delivery,  # Replace with the correct assignment ID
        )

        assignment = DeliveryAssignment.objects.get(id=out_for_delivery)
        assignment.status = 'OUT_FOR_DELIVERY'
        assignment.save()

        # You can add more logic here if needed

        return redirect('delivery_login')

    return HttpResponse('Invalid request method!')








from django.contrib.auth.decorators import login_required
from django.db.models import Subquery
from django.shortcuts import render
from .models import DeliveryAssignment, Order, User, user_payment, Cart, Cart_items, Product

# @login_required
# def ship_order(request):
#     # Fetch pending assignments related to products sold by the logged-in seller
#     pending_assignments = DeliveryAssignment.objects.filter(
#         status='PENDING',
#         order__userpayment__cart__in=Cart.objects.filter(
#             cart_items__product__seller_id=request.user
#         )
#     )

#     # Prepare assignment details for rendering
#     assignment_details = []
#     for assignment in pending_assignments:
#         # Fetch corresponding user details (assuming directly available from DeliveryAssignment)
#         user_details = {
#             'email': assignment.user.email,
#             'profile': assignment.user  # Assuming profile is a related field to User
#         }

#         assignment_details.append({
#             'assignment': assignment,
#             'user_details': user_details
#         })

#     context = {
#         'assignment_details': assignment_details,
#     }
#     return render(request, 'ship_order.html', context)



def ship_order(request):
    # Fetch pending assignments related to products sold by the logged-in seller
    pending_assignments = DeliveryAssignment.objects.filter(
        status='PENDING',
        order__userpayment__cart__in=Cart.objects.filter(
            cart_items__product__seller_id=request.user
        )
    )

    # Prepare assignment details for rendering
    assignment_details = []
    for assignment in pending_assignments:
        # Fetch corresponding user details (assuming directly available from DeliveryAssignment)
        user_details = {
             'first_name': assignment.user.profile.user.first_name,
            'last_name': assignment.user.profile.user.last_name,
            'email': assignment.user.email,
            'profile': assignment.user  # Assuming profile is a related field to User
        }
        
        # Fetch products associated with this assignment
        products_list = get_products_for_assignment(assignment)

        assignment_details.append({
            'assignment': assignment,
            'user_details': user_details,
            'products': products_list
        })

    context = {
        'assignment_details': assignment_details,
    }
    return render(request, 'ship_order.html', context)

def get_products_for_assignment(assignment):
    # Step 1: Get the associated Order
    order = assignment.order
    
    # Step 2: Get the associated UserPayment
    user_payment = order.userpayment
    
    # Step 3: Get the Cart associated with the UserPayment
    cart_items = Cart_items.objects.filter(cart=user_payment.cart)
    
    # Step 4: Iterate over the CartItems to get the associated Products
    products_list = []
    for cart_item in cart_items:
        product = cart_item.product
        # Assuming "product title image" means the first image associated with the product
        product_image_url = product.image_1.url if product.image_1 else None
        products_list.append({
            'product_name': product.product_name,
            'product_image': product_image_url
        })
    
    return products_list





def mark_as_shipped(request, assignment_id):
    if request.method == 'POST':
        assignment = DeliveryAssignment.objects.get(id=assignment_id)
        assignment.status = 'SHIPPED'
        assignment.save()
    return redirect('ship_order')


from django.shortcuts import render
from .models import DeliveryAssignment


def mark_shipped_multiple(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)

        # Extract the list of selected assignment IDs
        selected_assignment_ids = data.get('selected_assignments', [])

        # Update the status of selected assignments to "SHIPPED"
        DeliveryAssignment.objects.filter(id__in=selected_assignment_ids).update(status='SHIPPED')

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Assignments marked as shipped successfully'})

@login_required
def delivered_products(request):
    # Check if the logged-in user is a delivery boy
    if not hasattr(request.user, 'deliveryboy'):
        # Redirect or handle the case where the user is not a delivery boy
        # For example, you can display an error message or redirect them to a different page
        return render(request, 'not_delivery_boy.html')  # Create a template for this case

    # Fetching all delivery assignments where status is 'DELIVERED' and assigned to the current delivery boy
    delivered_assignments = DeliveryAssignment.objects.filter(delivery_boy=request.user.deliveryboy, status='DELIVERED')

    # Create a list to store details of delivered products
    delivered_products_list = []

    for assignment in delivered_assignments:
        try:
            # Fetch product details from the associated order
            product = assignment.order.userpayment.cart_items.first().product

            # Append the product details along with delivery details to the list
            delivered_products_list.append({
                'delivery_boy_name': request.user.deliveryboy.user.username,
                'delivered_product': product.product_name,
                'brand_name': product.brand_name,
                'stock': product.stock,
                'current_price': product.current_price,
                'image_1': product.image_1.url if product.image_1 else None,  # Assuming image_1 is an ImageField
                'delivered_at': assignment.assigned_at,
            })
        except Exception as e:
            # Handle any exceptions gracefully
            print(f"Error fetching product details: {e}")

    # Pass the list of delivered products to the template
    return render(request, 'delivered_products.html', {'delivered_products_list': delivered_products_list})




# views.py in the wallet app

# from django.shortcuts import render
# from .models import Wallet

# def wallet_page(request):
#     # Assuming you have implemented authentication and user login
#     wallet = Wallet.objects.get(user=request.user)
#     return render(request, 'wallet.html', {'wallet': wallet})



# views.py in the myauth app
# from decimal import Decimal
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Wallet

# def wallet_update(request):
#     if request.method == 'POST':
#         new_balance = request.POST.get('balance')
#         try:
#             wallet = Wallet.objects.get(user=request.user)
#         except Wallet.DoesNotExist:
#             # If Wallet does not exist for the user, create a new one
#             wallet = Wallet.objects.create(user=request.user, balance=new_balance)
#             messages.success(request, 'Wallet created successfully.')
#             return redirect('wallet_page')

#         # Convert new_balance to Decimal before adding it to the existing balance
#         new_balance_decimal = Decimal(new_balance)
#         wallet.balance += new_balance_decimal
#         wallet.save()
#         messages.success(request, 'Wallet balance updated successfully.')
#         return redirect('wallet_page')
#     return render(request, 'wallet_update.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Wallet, PaymentData
import razorpay

def wallet_update(request):
    if request.method == 'POST':
        new_balance = request.POST.get('balance')
        if new_balance is None:
            messages.error(request, "New balance is not provided.")
            return redirect('wallet_update')

        try:
            new_balance = float(new_balance)
        except ValueError:
            messages.error(request, "Invalid new balance value.")
            return redirect('wallet_update')

        # Initialize Razorpay client with your API key and secret
        client = razorpay.Client(auth=("rzp_test_UWsnOOpJ8l5HSD", "f35ZNp66fSEQVhGztOacN0jD"))

        # Create a Razorpay payment request
        amount = int(new_balance * 100)  # Convert new_balance to paise
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': 'receipt_id',  # Unique identifier for the payment
            'payment_capture': '1'  # Automatically capture the payment
        }
        payment = client.order.create(data=payment_data)

        # Get the payment ID from the payment response
        payment_id = payment['id']

        # Store payment_id and new_balance temporarily in session
        request.session['payment_id'] = payment_id
        request.session['new_balance'] = new_balance

        # Fetch wallet balance
        user = request.user
        wallet, created = Wallet.objects.get_or_create(user=user)
        wallet_balance = wallet.balance

        return render(request, 'wallet_payment.html', {'payment_id': payment_id, 'new_balance': new_balance, 'wallet_balance': wallet_balance})

    # Fetch wallet balance
    user = request.user
    wallet, created = Wallet.objects.get_or_create(user=user)
    wallet_balance = wallet.balance

    return render(request, 'wallet_update.html', {'wallet_balance': wallet_balance})


from django.shortcuts import redirect
from django.contrib import messages
from decimal import Decimal
from .models import Wallet, PaymentData

def wallet_page(request):
    if 'razorpay_payment_id' in request.GET:
        payment_id = request.GET.get('razorpay_payment_id')
        new_balance = request.session.get('new_balance')
        user = request.user
        wallet, created = Wallet.objects.get_or_create(user=user)

        # Fetch existing balance and convert it to Decimal
        existing_balance = Decimal(wallet.balance)

        # Update the balance by adding the new amount
        wallet.balance = existing_balance + Decimal(new_balance)
        wallet.save()

        # Store payment data
        PaymentData.objects.create(wallet=wallet, payment_id=payment_id, amount=new_balance)

        messages.success(request, "Payment successful! Updated balance: {}".format(wallet.balance))
        return redirect('wallet_update')  # Redirect to 'wallet_update' URL after successful payment
    else:
        messages.error(request, "Payment failed!")
        return redirect('wallet_update')  # Redirect to 'wallet_update' URL after failed payment







from django.shortcuts import render
from .models import Profile

def customer_detail_view(request):
    if request.user.is_authenticated:
        customer_profile = Profile.objects.get(user=request.user)
        return render(request, 'customer_detail.html', {'customer_profile': customer_profile})
    else:
        # Handle the case where the user is not authenticated
        # For example, redirect to the login page
        return redirect('login')  # Adjust this according to your login URL






#offer add by seller


from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Offer, Product, SellerProfile
from django import forms

def add_offer(request):
    class OfferForm(forms.ModelForm):
        class Meta:
            model = Offer
            fields = ['product', 'offer_name', 'discount_rate', 'start_date', 'end_date']

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            return HttpResponseRedirect('/success/')  # Redirect to a success page or wherever you need
    else:
        form = OfferForm()
    
    # Filter products based on the current user's seller profile
    seller_profile = SellerProfile.objects.get(user=request.user)
    products = Product.objects.filter(seller_id=seller_profile.user)
    
    return render(request, 'add_offer.html', {'form': form, 'products': products})


#about home
def about_home(request):

    return render(request, 'about_home.html' )



