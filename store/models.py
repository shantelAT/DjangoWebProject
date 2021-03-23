from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #a user can only have one customer and customer can only have one user
    name = models.CharField(max_length = 100, null= True)
    email = models.CharField(max_length=100, null= True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length= 200, null= True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url= self.image.url
        except:
            url=''
        return url

class Order(models.Model):                      #cart
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    date_ordered= models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default= False)
    transaction_id= models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()   #loop to get the order total of each item in cart ans sum them
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):                       #loop to get the total quantity in cart
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
            return shipping


    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):          # an item in cart
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):        #calc to get to total price for a item in car
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.CharField(max_length= 100, null=False)
    address= models.CharField(max_length= 100, null=False)
    city = models.CharField(max_length= 100, null=False)
    state = models.CharField(max_length= 100, null=False)
    zipcpode = models.CharField(max_length= 100, null=False)
    date_added = models.CharField(max_length= 100, null=True)

    def __str__(self):
        return self.address
