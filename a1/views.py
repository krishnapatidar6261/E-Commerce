from django.shortcuts import render,redirect
from . models import *
from django.conf import settings
from django.core.mail import send_mail
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'https://www.pythonanywhere.com'


@csrf_exempt
def create_checkout_session(request):

    #check user address available or not 

    data= json.load(request)

    print("data ***********************",data)
    #amount = int(json.load(request)['post_data'])

    amount = int(data['post_data'])
    product_id = int(data['pro_id'])
    product_qty = int(data['qty'])
    
    netprice = amount * product_qty
    
    print("Ammounr before *100 ",amount)
    amount= amount * 100
    
    session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': amount,
				},
			'quantity': product_qty,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + f'/success.html?session_id={{CHECKOUT_SESSION_ID}}',
		cancel_url=YOUR_DOMAIN + '/cancel.html',
        
        metadata={
            'product_id': product_id,
            'product_qty': product_qty,
            'net_price': netprice,
        }

        )
        
    
    return JsonResponse({'id': session.id})

def success(request):
    user=User()
    session_id = request.GET.get('session_id')
    print("success Usr: ",user)

    print("success Session id ",session_id)

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        product_id = session.metadata.product_id
        qty = session.metadata.product_qty
        
        net_price= session.metadata.net_price

        #order_id = session['order_id']
        transaction_id = session['payment_intent']
        user=User.objects.get(email=request.session['email'])
        product= Product.objects.get(pk=product_id)
        deli =Delivery.objects.get(user=user)
        Order.objects.create(

            user=user,
            product=product,
            product_qty=qty,
            product_price=product.product_price,
            total_price=net_price,
            transaction_id=transaction_id,
            deli= deli,
            

        )
   
    print("end")
    return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def order_details(request,pk):

    user= User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    order= Order.objects.filter(user=user, product=product).first()

    print("order ",order)
    print(product)

    print(order.product.product_name)
    return render(request,'order-detail.html',{'order':order})
    


def myorder(request):
    try:
        user=User.objects.get(email=request.session['email'])
        cart=Order.objects.filter(user=user)
        return render(request,'myorder.html',{'cart':cart})
    except:
        return render(request,'login.html')

def validate_email(request):
    email=request.GET.get('email')
    
    data={
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    
    return JsonResponse(data)

def check_old_pwd(request):
    user=User.objects.get(email=request.session['email'])
    old_pwd=request.GET.get('old_pwd')
    
    if user.password==old_pwd:
        data={
            'is_taken':True
        }
    else:
        data={
            'is_taken': False
        }
    
    return JsonResponse(data)

def check_pname(request):
    pname=request.GET.get('pname')
    user=User.objects.get(email=request.session['email'])
    data={
        'pname':Product.objects.filter(user=user, product_name=pname).exists()
    }
    print(data)
   
    return JsonResponse(data)
    
def check_login_email(request):
    email=request.GET.get('email')
    print('email',email)
    data={
        'is_taken':User.objects.filter(email__iexact=email).exists()
    }
    print(data)
    return JsonResponse(data)   


def get_net_price(request):

    if request.method =="POST":

        amount = request.POST.get('amount')

        return render(request, )



#@login_required(login_url='/login/')
def delevery_address(request):

    user= User.objects.get(email=request.session['email'])

    if request.method == "POST":
        amount = request.POST.get('amount')
        pro_id = request.POST.get('pro_id')
        product_qty=request.POST.get('product_qty')

        print("Amount*************************: ",amount)
        print("pro_id*************************: ",pro_id)
        print("product_qty*************************: ",product_qty)

        #creating address using post method
        if "address_updation" in request.POST:
            print("execute")

            if not Delivery.objects.filter(user=user).exists():

                Delivery.objects.create(
                    user=user,
                    address = request.POST.get('address'),
                    city = request.POST.get('city'),
                    state = request.POST.get('state'),
                    country = request.POST.get('country'),
                    postal_code = request.POST.get('postal_code'),
                    contact = request.POST.get('contact'),
                )

                deli= Delivery.objects.get(user=user)

                context={ 'deli':deli,
                         'net_price':amount,
                         'pro_id':pro_id,
                         'product_qty':product_qty,

                }

                return render(request,'order-summry.html',context)

            print("updated exce addr")
            #updating Address UsinG Post Method
            deli=Delivery.objects.get(user=user)

            deli.address = request.POST.get('address')
            deli.city = request.POST.get('city')
            deli.state = request.POST.get('state')
            deli.country = request.POST.get('country')
            deli.postal_code = request.POST.get('postal_code')
            deli.contact = request.POST.get('contact')

            deli.save()

            deli= Delivery.objects.get(user=user)
            product = Product.objects.get(pk= pro_id)
            context={ 'deli':deli,
                      'net_price':amount,
                      'pro_id':pro_id,
                      'product_qty':product_qty,
                      'product':product,

                }
            return render(request,'order-summry.html',context)



        if not Delivery.objects.filter(user=user).exists():

            amount = int(amount )* int(product_qty)

            context={
                         'net_price':amount,
                         'pro_id':pro_id,
                         'product_qty':product_qty,

                }
            return render(request,"order-address.html",context)
    
    
        deli = Delivery.objects.get(user=user)

        amount = int(amount )* int(product_qty)


        context={ 'deli':deli,
                  'net_price':amount,
                  'pro_id':pro_id,
                  'product_qty':product_qty,

                }
        return render(request,'updated-order-address.html',context)
        
    #Get Method Start  
    # if user is not exists we then go create html
    if not Delivery.objects.filter(user=user).exists():

        context={
                    'net_price':amount,
                    'pro_id':pro_id,
                    'product_qty':product_qty,
                }
        return render(request,"order-address.html",context)
    
    
    deli = Delivery.objects.get(user=user)
    return render(request,'updated-order-address.html',{'deli':deli})

    
   


def index(request):
    product=Product.objects.all()
    return render(request,'index.html',{'product':product})
    #return redirect('index',{'product':product})

def seller_index(request):
    
    return render(request,'seller-index.html')


def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            name=request.POST['cf_name'],
            email=request.POST['cf_email'],
            subject=request.POST['cf_subject'],
            message=request.POST['cf_message'],
        )
        msg="Contacted Successfully Wait For Email"
        return render(request,'contact.html',{'msg':msg})
    else:
        return render(request,'contact.html')

def blog(request):
    
    return render(request,'blog.html')

def blog_post(request):
    
    comments=Comment.objects.all().order_by("-id")
    if request.method=="POST":
        Comment.objects.create(
        name=request.POST['name'],
        email=request.POST['email'],
        comment=request.POST['comment'],
        
        )
        
        return render(request,'blog-detail.html',{'comments':comments})
        
    else:
        return render(request,'blog-detail.html',{'comments':comments})

def register(request):
    if request.method=="POST":
        try: 
            User.objects.get(email=request.POST['email'])
            msg="Email Already Register"
            return render(request,'register.html',{'msg':msg})
        except:
            
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                password=request.POST['password'], 
                profile_pic=request.FILES['profile_pic'],
                user_type=request.POST['usertype']
                
                )
                msg="Account created Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password and Confirm Password Does Not Matched"
                return render(request,'register.html',{'msg':msg})
            
        

    else:
        return render(request,'register.html')
    
def login(request):
    if request.method=="POST":
        if request.POST['email']=="" or request.POST['password']=="":
           
            msg="Please Enter User and Password"
            return render(request,'login.html',{'msg':msg})
        
        else:
            try:
                user=User.objects.get(email=request.POST['email'])
                product=Product.objects.all()
                if user.password==request.POST['password']:
                    if user.user_type=="buyer":
                        request.session['email']=user.email
                        request.session['fname']=user.fname
                        request.session['profile_pic']=user.profile_pic.url
                        try:
                            user=User.objects.get(email=request.session['email'])
                            cart=Cart.objects.filter(user=user,payment_status=False)
                            request.session['cart_count']=len(cart)
                        except:
                            pass
                        
                        try:
                            user=User.objects.get(email=request.session['email'])
                            wishlist=Wishlist.objects.filter(user=user)
                            request.session['wishlist_count']=len(wishlist)
                            
                        except:
                            pass                         
                        
                        return render(request,'index.html',{'product':product})
                    else:
                        request.session['email']=user.email
                        request.session['fname']=user.fname
                        request.session['profile_pic']=user.profile_pic.url
                        return render(request,'seller-index.html')
                else:
                    msg="Incorrect User Or Password"
                    return render(request,'login.html',{'msg':msg})
            except:
                msg="Email Not Register"
                return render(request,'login.html',{'msg':msg})
            
    else:
        return render(request,'login.html')
        
def logout(request):
    
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_pic']
        del request.session['cart_count']
        del request.session['wishlist_count']
        return render(request,'login.html')
    except:
        return render(request,'login.html')
    
def update_profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        try:
            user.profile_pic=request.FILES['profile_pic']       
            
        except:
            pass
        request.session['profile_pic']=user.profile_pic.url

        user.save()
        msg="Profile Updated Successfully"
        if user.user_type=="buyer":
            return render(request,'index.html',{'msg':msg,'user':user})
        else:
            return render(request,'seller-index.html',{'msg':msg,'user':user})
        
    else:
        if user.user_type=="buyer":
            return render(request,'update-profile.html',{'user':user})
        else:
            return render(request,'seller-update-profile.html',{'user':user})


def change_password(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        if user.password==request.POST['old_pwd']:
            if request.POST['new_pwd']==request.POST['cnew_pwd']:
                user.password=request.POST['new_pwd']
                user.save()
                return redirect('logout')
            else:
                if user.user_type=="buyer":
                    msg="New and Confirm New Password Does Not Matched"
                    return render(request,'change-password.html',{'msg':msg,'email':user.email})
                else:
                    msg="New and Confirm New Password Does Not Matched"
                    return render(request,'seller-change-password.html',{'msg':msg,'email':user.email})
                    
        else:
            if user.user_type=="buyer":
                msg="Old Password Does Not Matched"
                return render(request,'change-password.html',{'msg':msg})
            else:
                msg="Old Password Does Not Matched"
                return render(request,'seller-change-password.html',{'msg':msg})

            
    else:
        if user.user_type=="buyer":
            return render(request,'change-password.html')
        else:
            return render(request,'seller-change-password.html')

    

def forgot_password(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            subject = 'Email For Forgot Password'
            otp=random.randint(1000,9999)
            message = "Hello "+ user.fname+" Your Forgot Password OTP is "+ str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            
            msg="OTP Send Successfully"
            return render(request,'verify-OTP.html',{'msg':msg,'email':user.email,'otp':otp})
        except:
            
            msg="Email Not Register"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')
    
def verify_OTP(request):
    if request.method=="POST":
        email=request.POST['email']
        otp=request.POST['otp']
        uotp=request.POST['uotp']
        if otp==uotp:
           
            return render(request,'update-password.html',{'email':email})
        else:
            msg="Incorret OTP"
            return render(request,'verify-OTP.html',{'msg':msg,'email':email,'otp':otp})

    else:       
        return render(request,'verify-OTP.html')
    
def update_password(request):
    email=request.POST['email']
    if request.method=="POST":
       
        if request.POST['new_pwd']==request.POST['cnew_pwd']:
            user=User.objects.get(email=email)
            user.password=request.POST['new_pwd']
            user.save()
            msg="Password Updated Successfully"
            return render(request,'login.html',{'msg':msg})
        
        else:
            msg="Password and confirm Password Does Not Matched"
            return render(request,'update-password.html',{'msg':msg,'email':email})
            
    else:
        return render(request,'update-password.html')
    
def terms_conditions(request):
    
    return render(request,'terms&conditions.html')


def couple_dress(request):
    
    return render(request,'couple-dress.html')


def electronics(request):               #electronics page functions
    product=Product.objects.filter(product_category="Electronics")
    return render(request,'electronics.html',{'product':product})

def iron(request):
    return render(request,'iron.html')

def laptop(request):
    return render(request,'laptop.html')

def accessories(request):
    return render(request,'accessories.html')

def jeans(request):                           #jeans page functions
    return render(request,'jeans.html')

def men(request):                           #men page functions
    product=Product.objects.filter(product_category="Men")
    return render(request,'men.html',{'product':product})

def women(request):                             #women page functions
    product=Product.objects.filter(product_category="Women")
    return render(request,'women.html',{'product':product})

def baby_kids(request):                             #baby_kids page functions
    product=Product.objects.filter(product_category="Baby & Kids")
    return render(request,'baby&kids.html',{'product':product})

def books(request):                             #books page functions
    product=Product.objects.filter(product_category="Books")
    return render(request,'books.html',{'product':product})

def home_kitchen(request):                             #home & kitchen page functions
    product=Product.objects.filter(product_category="Home & Kitchens")
    return render(request,'home&kitchen.html',{'product':product})

def more_stores(request):                             #more_stores page functions
    return render(request,'index.html')



def add_product(request):
    if request.method=="POST":
        seller=User.objects.get(email=request.session['email'])
        Product.objects.create(
            seller=seller,
            product_category=request.POST['product_category'],
            product_name=request.POST['product_name'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image'],
        )
        msg="Product Added Successfully"
        return render(request,'add-product.html',{'msg':msg})
    else:
        return render(request,'add-product.html')
    
def view_product(request):
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)      #filter work like where clouse
    
    return render(request,'view-product.html',{'products':products})

def product_detail(request,pk):
    product=Product.objects.get(pk=pk)
    try:
        user=User.objects.get(email=request.session['email'])
        if user.user_type=='buyer':
            wishlist_flag=False
            cart_flag=False
            try:
                Wishlist.objects.get(user=user,product=product)
                wishlist_flag=True
                      
            except:
                pass
            try:
                Cart.objects.get(user=user,product=product,payment_status=False)
                cart_flag=True
                      
            except:
                pass
            return render(request,'buyer-product-detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag}) 
               # return render(request,'buyer-product-detail.html',{'product':product})       
        else:
            return render(request,'product-detail.html',{'product':product})
    except:
            return render(request,'buyer-product-detail.html',{'product':product})       
        
        

def seller_edit_product(request,pk):
       
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_name=request.POST['product_name']
        product.product_price=request.POST['product_price']
        product.product_desc=request.POST['product_desc']
        product.product_category=request.POST['product_category']
        try:
            product.product_image=request.FILES['product_image']
        except:
            pass
        product.save()
        msg="Update Successfully"
        return render(request,'seller-edit-product.html',{'msg':msg,'product':product})
    else:
        return render(request,'seller-edit-product.html',{'product':product})

def seller_delete_product(request,pk):
    
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('view-product')

def add_to_wishlist(request,pk):
    
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    Wishlist.objects.create(
        user=user,
        product=product,
    )
    return redirect('mywishlist')
    
def wishlist(request):
    try:
        user=User.objects.get(email=request.session['email'])
        wishlist=Wishlist.objects.filter(user=user)
        request.session['wishlist_count']=len(wishlist)
        return render(request,'mywishlist.html',{'wishlist':wishlist})
    except:
        return render(request,'login.html')

def remove_from_wishlist(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)

    wishlist=Wishlist.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect('mywishlist')


def add_to_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    Cart.objects.create(
        user=user,
        product=product,
        product_qty=1,
        product_price=product.product_price,
        total_price=product.product_price
    )
    
    return redirect('mycart')

def mycart(request):
    try:
        net_price=0
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user,payment_status=False)
        request.session['cart_count']=len(cart)
        
        for i in cart:
            net_price=net_price + i.total_price
        
        return render(request,'mycart.html',{'cart':cart,'net_price':net_price})
    except:
        return render(request,'login.html')

def remove_from_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    cart=Cart.objects.get(user=user,product=product,payment_status=False)
    
    cart.delete()
    return redirect('mycart')

def change_qty(request):
    pk=request.POST['pk']
    product_qty=1
    product_qty=int(request.POST['product_qty'])
    cart=Cart.objects.get(pk=int(pk))
    cart.product_qty=product_qty
    cart.total_price=cart.product_price * product_qty
    cart.save()
    return redirect('mycart')
       
       
def seller_view_order(request):
    user_seller=User.objects.get(email=request.session['email'])
    product = Product.objects.filter(seller=user_seller)

    order = Order.objects.filter(product__in=product,order_approve=False )
    
    
    return render(request,'seller-view-order.html',{'myorder':order})

def seller_view_order_detail(request,pk):

    product = Product.objects.get(pk=pk)       

    order = Order.objects.filter(product=product,).first()

    return render(request,'seller-view-order-detail.html',{'order':order})

def shiped_approve(request,pk):

    order = Order.objects.get(pk=pk)

    order.order_approve = True
    order.save()

    user_seller=User.objects.get(email=request.session['email'])
    product = Product.objects.filter(seller=user_seller)

    order = Order.objects.filter(product__in=product,order_approve=False )

    return render(request,'shiped.html',{'order':order})

def shiped(request):
    user_seller=User.objects.get(email=request.session['email'])
    product = Product.objects.filter(seller=user_seller)

    order=Order.objects.filter(product__in=product,order_approve=True )

    return render(request, 'shiped.html',{'order':order})

