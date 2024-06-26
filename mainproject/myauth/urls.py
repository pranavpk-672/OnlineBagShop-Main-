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
    path('about_home/',views.about_home,name='about_home'),
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
        path('customer/', views.customer_detail_view, name='customer_detail'),



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
    path('register_delivery_boy/', views.register_delivery_boy, name='register_delivery_boy'),



path('cartt/', views.cartt, name='cartt'),
path('admin_prodview/', views.admin_prodview, name='admin_prodview'),
path('reviews/', views.admin_proddview, name='reviews'),
path('prod_detail_review/<int:product_id>/', views.prod_detail_review, name='prod_detail_review'),
path('notification_view/', views.notification_view, name='notification_view'),
path('sellers_item/', views.sellers_item, name='sellers_item'),
path('seller-products/<int:seller_id>/', views.seller_products_view, name='seller_products_view'),








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
        path('activate_seller/<int:user_id>/', views.activate_seller, name='activate_seller'),
    path('deactivate_seller/<int:user_id>/', views.deactivate_seller, name='deactivate_seller'),

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

    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),


    #delivery_boy_registration
    path('deliveryboy_registration/', views.deliveryboy_registration, name='deliveryboy_registration'),

    path('add_delivery_boys/',views.add_delivery_boys,name="add_delivery_boys"),
    path('delivery_login/',views.delivery_login,name="delivery_login"),
    path('Change_password/', views.Change_password, name='Change_password'),
    path('delivery_password/', views.delivery_password, name='delivery_password'),

     path('delivery_delivered/',views.delivery_delivered,name="delivery_delivered"),



 #purchase history view
    path('purchasing_histor/', views.purchasing_histor, name='purchasing_histor'),
    path('purchasing_history/', views.purchasing_history, name='purchasing_history'),
    path('product_purchase_details/', views.product_purchase_details, name='product_purchase_details'),
    path('cart_items_list/<int:cart_id>/', views.product_cart_details, name='cart_items_list'),
    path('reviews/', views.list_reviews, name='list_reviews'),

path('delivery_add_excel/', views.delivery_add_excel, name='delivery_add_excel'),
#count not correct
 path('adminreg/', views.dashboardd, name='dashboardd'),
#  path('generate-pdf/<int:user_id>/', views.generate_user_payment_pdf, name='generate_user_payment_pdf'),
path('generate-latest-payment-pdf/<int:user_id>/', views.generate_user_latest_payment_pdf, name='generate_user_latest_payment_pdf'),
 path('delivery_vieww/', views.delivery_vieww, name='delivery_vieww'),
 path('activate_delivery_boy/<int:delivery_boy_id>/', views.activate_delivery_boy, name='activate_delivery_boy'),
 path('deactivate_delivery_boy/<int:delivery_boy_id>/', views.deactivate_delivery_boy, name='deactivate_delivery_boy'),
 path('generate_coupon/',views.generate_coupon, name='generate_coupon'),
path('coupon/',views.coupon, name='coupon'),
# path('coupon_list/',views.coupon_list, name='coupon_list'),
    path('coupon_list/', views.display_seller_coupons, name='seller_coupons'),
    path('seller_view_review/', views.seller_view_review, name='seller_view_review'),

    path('seller_view_notification/', views.seller_view_notification, name='seller_view_notification'),
    path('download-pdf/', views.download_low_stock_products_pdf, name='download_low_stock_products_pdf'),



# path('seller_product_user_view/', views.seller_product_user_view, name='seller_product_user_view'),

path('seller_product_user_view/', views.list_purchased_users_of_seller, name='list_purchased_users_of_seller'),
path('seller_product_user_view/<int:user_id>/', views.view_purchased_products, name='view_purchased_products'),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),


    path('purchase_orders/', views.purchase_orders, name='purchase_orders'),

    path('seller/product/<int:product_id>/', views.seller_prod_detail_reviewsss, name='seller_product_detail'),
    path('purchase-details/', views.purchase_detailsss, name='purchase_details'),
        path('seller_display_product/', views.seller_display_product, name='seller_display_product'),

    path('new-orders/', views.new_orders, name='new_orders'),
    path('trackmyorder/', views.trackmyorder, name='trackmyorder'),

    path('delivery/update_status/', views.update_delivery_status, name='update_delivery_status'),
    path('view-products/', views.view_products_user, name='view_products'),
    path('create_otp/', views.create_otp, name='create_otp'),
    path('verify_otp_delivery/', views.verify_otp_delivery, name='verify_otp_delivery'),
    path('ship_order/',views.ship_order,name='ship_order'),
    path('mark-shipped/<int:assignment_id>/', views.mark_as_shipped, name='mark_shipped'),
    path('delivered-products/', views.delivered_products, name='delivered_products'),
    path('wallet/update/', views.wallet_update, name='wallet_update'),
    path('wallet/payment/success/', views.payment_success, name='payment_success'),
    path('wallet_page/', views.wallet_page, name='wallet_page'),
    path('wallet_page/', views.wallet_page, name='wallet_page'),

    path('checkout_view_wallet/', views.checkout_view_wallet, name="checkout_view_wallet"),

    path('mark_shipped_multiple/', views.mark_shipped_multiple, name='mark_shipped_multiple'),


    path('add_offer/', views.add_offer, name='add_offer'),





]

#image
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)