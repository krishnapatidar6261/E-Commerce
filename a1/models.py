from django.db import models


# Create your models here.
class User(models.Model):
    
    fname=models.CharField( max_length=50)
    lname=models.CharField( max_length=50)
    password=models.CharField( max_length=50)
    email=models.EmailField()
    profile_pic=models.ImageField(upload_to='profile_pic/',default="usericon.jpg")
    user_type=models.CharField(max_length=50, default="buyer")
    
    
    def __str__(self):
        
        return self.email
    
class Contact(models.Model):
    
    name=models.CharField( max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.subject
    
class Comment(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField()
    comment=models.CharField(max_length=50)
    time=models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.email
    
    
class Product(models.Model):
    seller=models.ForeignKey(User, on_delete=models.CASCADE)
    choice=(
        
        ("Electronics","Electronics"),  
        ("Men","Men"),  
        ("Women","Women"),  
        ("Baby & Kids","Baby & Kids"),  
        ("Home & Kitchens","Home & Kitchens"),  
        ("Books","Books"),  
        ("Other","Other"),  
    )
    product_category=models.CharField(max_length=50, choices=choice, default="Others")
    product_name=models.CharField(max_length=50)
    product_price=models.PositiveIntegerField()
    product_desc=models.CharField(max_length=300,default="")
    product_date=models.DateField(auto_now_add=True)
    product_image=models.ImageField(upload_to="product_image")
    
    def __str__(self):
        
        return self.seller.fname+" - "+self.product_name
    
class Wishlist(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.product.name+"-"+self.user.name
    
class Wishlist(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.product.product_name+"-"+self.user.fname
    
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty=models.PositiveIntegerField(default=1)
    product_price=models.PositiveIntegerField()
    payment_status=models.BooleanField(default=False)
    total_price=models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return self.user.fname+"-"+ self.product.product_name


class Delivery(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.PositiveIntegerField()
    contact = models.PositiveIntegerField()


    def __str__(self) -> str:
        return self.user.email

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) #user should considerd as a buyer
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    deli = models.ForeignKey(Delivery, on_delete=models.CASCADE,null=True,blank=True)
    product_qty=models.PositiveIntegerField(default=1)
    product_price=models.PositiveIntegerField()
    total_price=models.PositiveIntegerField(default=0)
    transaction_id = models.TextField(default=None,null=True,blank=True)
    order_approve = models.BooleanField(default=False, )
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user.email

