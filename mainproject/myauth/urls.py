from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import path
from myauth import views


from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

from django.conf import settings
from django.conf.urls.static import static

 


urlpatterns = [

    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    path('log/',views.log,name='log'),
    path('home/',views.home,name='home'),
    path('adminreg/',views.adminreg,name='adminreg'),
    path('adminn/',views.adminn,name='adminn'),
    path('abouttt/',views.abouttt,name='abouttt'),
    path('con/',views.con,name='con'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('update-profile/',views.update_profile,name='update-profile'),
    path('sell/',views.sell,name='sell'),
    path('signupsell/',views.signupsell,name='signupsell'),
    path('sellersig/',views.sellersig,name='sellersig'),
    path('sell_upd/',views.seller_profile_update,name='sell_upd'),

    path('sellerr/',views.sellerr,name='sellerr'),
    path('sellviews/',views.sellviews,name='sellviews'),
    path('userviewss/',views.userviewss,name='userviewss'),


    #selleer approval
    path('sellor_approval/',views.sellor_approval,name="sellor_approval"),
    path('approve_seller/<int:seller_id>/', views.approve_seller, name='approve_seller'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),

    path('selleraddprod/',views.selleraddprod,name='selleraddprod'),
    path('add_product/',views.add_product,name='add_product'),

    path('add_category/',views.add_category,name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
    path('sub_category_list/<int:category_id>/', views.sub_category_list, name='sub_category_list'),

    #seller block
    path('block_seller/<int:seller_id>/',views.block_seller,name="block_seller"),
    
    #Delete seller
     path('delete_seller/<int:seller_id>/',views.delete_seller,name="delete_seller"),


    path('category_add/',views.category_add,name="category_add"),
    path('add_sub_category/<int:category_id>/', views.add_sub_category, name='add_sub_category'),
     path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

     path('delete_sub_category/<int:sub_category_id>/', views.delete_sub_category, name="delete_sub_category"),






#product detailed view
path('prodetailview/<int:product_id>/', views.prodetailview, name='prodetailview'),
   # path('products/<int:product_id>/', views.product_detail, name='product_detail'),



path('prodetailview_index/<int:product_id>/', views.prodetailview_index, name='prodetailview_index'),

# ALL product view
    path('productallview/', views.productallview, name='productallview'),
    path('productallview_index/', views.productallview_index,name="productallview_index"),
    path('productscategorylist_index/<int:category_id>/', views.productscategorylist_index,name="productscategorylist_index"),



path('cartt/', views.cartt, name='cartt'),
path('admin_prodview/', views.admin_prodview, name='admin_prodview'),



# path('seller_prodview/', views.seller_prodview, name='seller_prodview'),

path('seller_prodview/', views.seller_prodview, name='seller_prodview'),
    path('seller/products/update/<int:product_id>/', views.update_product, name='update_product'),


# list category items
path('category/<str:category>/', views.category_detail, name='category_detail'),
path('subcategory/<str:category>/', views.subcategory_detail, name='subcategory_detail'),
path('brand/<str:category>/', views.brand_detail, name='brand_detail'),



path('add_product/', views.add_product, name='add_product'),
path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),



path('view_cart/', views.view_cart, name='view_cart'),
path('delete_cartitem/<int:cart_id>/', views.delete_cartitem, name='delete_cartitem'),


path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
path('view_wishlist/', views.view_wishlist, name='view_wishlist'),
path('delete_wishlistitem/<int:item_id>/', views.delete_wishlistitem, name='delete_wishlistitem'),

path('productscategorylist/<int:category_id>/', views.productcategorylistview, name='product_category_list'),

path('productssubcategorylist/<int:subcategory_id>/', views.productsubcategorylistview, name='product_sub_category_list'),




 path('search/', views.search_products, name='search_products'),
 path('autocomplete/', views.autocomplete_search, name='autocomplete_search'),

  path('update_cart_item_quantity/<int:cart_item_id>/<int:new_quantity>/<int:currentPrice>', views.update_cart_item_quantity, name='update_cart_item_quantity'),



path('checkout/', views.checkout_view, name='checkout_view'),
path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

path('payment_success/', views.payment_success, name='payment_success'),

#activate and  deactivate
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),

    path('payment_history/', views.payment_history, name='payment_history'),


 path('product_review_page/<int:product_id>/', views.product_review_page, name='product_review_page'),

 path('submit_review', views.submit_review, name='submit_review'),

    #forget pass
    #path('request-reset-email/',views.RequestResetEmailView.as_view(),name="request-reset-email"),
    #path("set-new-password/<uidb64>/<token>",views.SetNewPassword.as_view(),name="set-new-password"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

    #authentication

    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate')

]

#image
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)