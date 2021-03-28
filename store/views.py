import json
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  #messages on login and register pages

from django.contrib.auth import authenticate, login, logout


import datetime
from .models import *
from .forms import CreateUserForm


def registerPage(request):
	form = CreateUserForm

	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user.form.cleaned_data.get('username')
			messages.success(request, 'Account was successfully created for'+ user)
			return redirect('login')


	context ={'form': form}
	return render(request, 'store/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('store')

	context ={}
	return render(request, 'store/login.html', context)

#----------------- STORE PAGE VIEW -----------------

def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)   #quering and odject or creating one
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:						#GUEST USER
		try :  #temp - provide cookie on first reload
			cart = json.loads(request.COOKIES['cart'])		#reflect the cart cookie on the cart page
		except:
			cart = {}
			print("cart:", cart)


		items = []
		order  = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

		for i in cart:
			try: 					#incase item is removed from database - guest user
				cartItems += cart[i]["quantity"]

				product = Product.objects.get(id=i)		#key are product id
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {					#cart built out for guest; user not in db
					'product':{
						'id': product.id,
						'name': product.name,
						'price': product.price,
						'imageUrl': product.imageUrl,
						},
					'quantity':cart[i]['quantity'],
					'get_total': total
				}
				items.append(item)
			except:
				pass

	products = Product.objects.all()
	context = {'products': products, 'cartItems':cartItems }
	return render(request, 'store/store.html', context)

#----------------- CART PAGE VIEW -----------------

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer		#
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()		#quering and odject or creating one
		cartItems = order.get_cart_items

	else:						#GUEST USER
		try :  #temp - provide cookie on first reload
			cart = json.loads(request.COOKIES['cart'])		#reflect the cart cookie on the cart page
		except:
			cart = {}
			print("cart:", cart)


		items = []
		order  = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

		for i in cart:
			try: 					#incase item is removed from database - guest user
				cartItems += cart[i]["quantity"]

				product = Product.objects.get(id=i)		#key are product id
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {					#cart built out for guest; user not in db
					'product':{
						'id': product.id,
						'name': product.name,
						'price': product.price,
						'imageUrl': product.imageUrl,
						},
					'quantity':cart[i]['quantity'],
					'get_total': total
				}
				items.append(item)
			except:
				pass

	context = {'items': items, 'order': order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


#----------------- CHECKOUT PAGE VIEW -----------------

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)   #quering and odject or creating one
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:						#GUEST USER
		try :  #temp - provide cookie on first reload
			cart = json.loads(request.COOKIES['cart'])		#reflect the cart cookie on the cart page
		except:
			cart = {}
			print("cart:", cart)


		items = []
		order  = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

		for i in cart:
			try: 					#incase item is removed from database - guest user
				cartItems += cart[i]["quantity"]

				product = Product.objects.get(id=i)		#key are product id
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {					#cart built out for guest; user not in db
					'product':{
						'id': product.id,
						'name': product.name,
						'price': product.price,
						'imageUrl': product.imageUrl,
						},
					'quantity':cart[i]['quantity'],
					'get_total': total
				}
				items.append(item)
			except:
				pass

	context = {'items': items, 'order': order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):  #updating values in cart on cart page
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:' , action )
	print('productId:' , productId )

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)   #quering and odject or creating one

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp() #id sent to back
	data = json.loads(request.body) #parse data
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer = customer,
				order =order,
				address= data['shipping']['address'],
				city = data['shipping']['city'],
				state =data['shipping']['state'],
				#zipcode = data['shipping']['zipcode'],
				)


	else:
		print('User is not logged in')  #send info to back end for users who are looged in
		'''
		print('COOKIES:', request.COOKIES)
		name = data['form']['name']
		email = data[ 'form']['email']

		cookieData = cookieC

		'''
	return JsonResponse('Payment Complete', safe=False)  #display that order was complete after cx place order
