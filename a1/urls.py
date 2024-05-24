from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('seller/',views.seller_index,name='seller-index'),
    path('contact/',views.contact,name='contact'),
    path('blog/',views.blog,name='blog'),
    path('blog-post/',views.blog_post,name='blog-post'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('update-profile/',views.update_profile,name='update-profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-OTP/',views.verify_OTP,name='verify-OTP'),
    path('update-password/',views.update_password,name='update-password'),
    path('terms&conditions/',views.terms_conditions,name='terms&conditions'),
    path('electronics/',views.electronics,name='electronics'),  #Electronics Page Url
    path('iron/',views.iron,name='iron'),
    path('laptop/',views.laptop,name='laptop'),
    path('accessories/',views.accessories,name='accessories'),  
    path('men/',views.men,name='men'),                          # Men page Url
    path('jeans/',views.jeans, name='jeans'),  
    path('women/',views.women,name='women'),                          # Women page Url
    path('baby&kids/',views.baby_kids,name='baby&kids'),              #baby & kids page Url
    path('books/',views.books,name='books'),                          # books page Url
    path('home&kitchen/',views.home_kitchen,name='home&kitchen'),     # home&kitchen page Url
    path('more-stores/',views.more_stores,name='more-stores'),        # more-stores page Url
    path('add-product/',views.add_product,name='add-product'),
    path('view-product/',views.view_product,name='view-product'),
    path('product-detail/<int:pk>/',views.product_detail,name='product-detail'),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>/',views.seller_delete_product,name='seller-delete-product'),
     path('add-to-wishlist/<int:pk>',views.add_to_wishlist,name='add-to-wishlist'),
    path('mywishlist', views.wishlist,name='mywishlist'),
    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('add-to-cart/<int:pk>',views.add_to_cart, name='add-to-cart'),
    path('mycart', views.mycart, name='mycart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('change-qty',views.change_qty, name='change-qty'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success.html/', views.success, name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('myorder/', views.myorder,name='myorder'),
    path('order-details/<int:pk>',views.order_details, name="order-details"), # Buyer View Their detaila
    
    path('get-net/', views.get_net_price, name="get-net"),

    path('order-address/', views.delevery_address, name="order-address"),

    path('seller-view-order/', views.seller_view_order, name='seller-view-order'),
    path('seller-view-order-detail/<int:pk>', views.seller_view_order_detail, name='seller-view-order-detail'),
    path('shipped-approved/<int:pk>', views.shiped_approve , name="shiped-approve"),
    path('shiped/', views.shiped , name="shiped"),


    path('ajax/validate-email/', views.validate_email, name='ajax/validate-email/'),
    path('check-old-pwd/', views.check_old_pwd, name='check-old-pwd/'),
    path('check-pname/', views.check_pname, name="check-pname"),
    path('login-check-email//', views.check_login_email, name="login-check-email/")

]
