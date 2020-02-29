from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Sum
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Pizza, Topping, Dinner, Salad, Pasta, Sub, Cart, Order
from django.core import serializers
from decimal import Decimal
import json


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main_app"))
    else:    
        return render(request, "orders/index.html")

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("main_app"))
    else:
        if request.method == "POST":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['user_name']
            email = request.POST['email']
            password1 = request.POST['password']
            password2 = request.POST['confirm_password']

            if password1==password2:
                if User.objects.filter(username__iexact=username).exists():
                    messages.info(request, "Username already taken")
                    return HttpResponseRedirect(reverse("registeration"))
                elif User.objects.filter(email__iexact=email).exists():
                    messages.info(request, "Email unavaialable")
                    return HttpResponseRedirect(reverse("registeration"))
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email, first_name=firstname, last_name=lastname)
                    user.save()
                    return HttpResponseRedirect(reverse("login"))
            else:
                messages.info(request,"Password didn't match")
                return HttpResponseRedirect(reverse("registeration"))
        else:
            return render(request, "orders/register.html")

@csrf_exempt
def owner_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                cmplt_order_id = int(request.POST["cmplt_info"])  
                order_done = Order.objects.get(id=cmplt_order_id)
                order_done.o_status = True
                order_done.save()
                return JsonResponse({"success": True})
            else:
                all_carts = Cart.objects.filter(user_id__contains=request.user.id)
                cart_length = len(all_carts)

                all_orders = Order.objects.all()
                count = 0
                even_list = []
                odd_list = []
                for order in all_orders:
                    if count % 2 == 0:
                        even_list.append(order)
                    else:
                        odd_list.append(order)
                    count += 1
                owner_context = {"len": cart_length, "even": even_list, "odd": odd_list}
                return render(request, "orders/owner_page.html", owner_context)
        else:
            return HttpResponseRedirect(reverse("main_app"))
    else:
        return HttpResponseRedirect(reverse("index"))                


@login_required
def orders(request):
    if request.method =="POST":
        all_carts = Cart.objects.filter(user_id__contains=request.user.id) 
        final_price = 0.00
        final_order = ""
        order_no = 1
        for cart in all_carts:
            final_order += str(order_no) + ") " + cart.order_contents + " ;"
            final_price += float(cart.total_price)
            order_no += 1
        final_price = round(final_price, 2)      
        fo = Order(user_id = request.user.id, order_price = final_price, order_details = final_order, user_name = request.user)
        fo.save()
        all_carts = Cart.objects.filter(user_id__contains=request.user.id)
        Cart.objects.filter(user_id__contains=request.user.id).delete()
        all_orders = Order.objects.filter(user_id__contains=request.user.id)
        cart_length = len(all_carts)
        orders_context = {"orders": all_orders, "len" : cart_length}
        return HttpResponseRedirect(reverse("orders"))
    else:
        all_carts = Cart.objects.filter(user_id__contains=request.user.id)
        all_orders = Order.objects.filter(user_id__contains=request.user.id)
        cart_length = len(all_carts)
        orders_context = {"orders": all_orders, "len" : cart_length}
        return render(request, "orders/orders.html", orders_context)
 

@login_required
@csrf_exempt
def delete(request):
    if request.method == "POST":
        if 'del_info' in request.POST:
            del_order_id = int(request.POST['del_info'])
            Cart.objects.filter(id=del_order_id).delete() 
        elif 'o_del' in request.POST:
            del_order_id = int(request.POST['o_del'])
            Order.objects.get(id=del_order_id).delete()
        return JsonResponse({"success": True})
    else:
        return HttpResponseRedirect(reverse("main_app"))             

@login_required
def cart(request):
    if request.method == "POST":
        info = request.POST['select_name']
        if 'pizza' in info:
            price = float(info[info.find('pizza') +6:])
            toppings_number = int(info[0])
            size = info[1:6]
            pizza_name = info[6:info.find('pizza') +5]
            pza_tpngs = []
            if toppings_number > 0 and toppings_number < 4:
                for i in range(toppings_number):
                    pza_tpngs.append(request.POST["pizzaselect"+str(i)])
            tpngs = "Toppings: "

            if toppings_number > 0 and toppings_number < 4:
                for top in pza_tpngs:
                    if pza_tpngs.index(top) != len(pza_tpngs) - 1:
                        tpngs += top + ", "
                    else:
                        tpngs += top + ". "  
            else:
                tpngs = ""          
            o = Cart(user_id=request.user.id, order_contents=pizza_name + "(" + size + ") " + tpngs, total_price = price, user_name = request.user)  
            o.save()  
            return HttpResponseRedirect(reverse("main_app"))
        elif 'dinner' in info:
            price = float(info[info.find('dinner') +7:])
            size = info[0:5]
            dinner_name = info[5:info.find(')')]
            o = Cart(user_id=request.user.id, order_contents=dinner_name + "(" + size + ") " , total_price = price, user_name = request.user)  
            o.save()
            return HttpResponseRedirect(reverse("main_app"))
        elif 'salad' in info:
            salad_name = info[:info.find('#')]
            digit_place=0
            for a in info:
                if a.isdigit():
                    digit_place = info.find(a)
                    break
            price = float(info[digit_place:])           
            o = Cart(user_id=request.user.id, order_contents=salad_name , total_price = price, user_name = request.user)  
            o.save()
            return HttpResponseRedirect(reverse("main_app"))   
        elif 'pasta' in info:
            pasta_name = info[:info.find('#')]
            price = float(info[info.find('#') + 6:]) 
            o = Cart(user_id=request.user.id, order_contents=pasta_name , total_price = price, user_name = request.user)  
            o.save()
            return HttpResponseRedirect(reverse("main_app"))  
        else:
            size = info[1:6]
            extras = []
            if 'newCheckBox0' in request.POST:
                extras.append(request.POST['newCheckBox0'])
            if 'newCheckBox1' in request.POST:
                extras.append(request.POST['newCheckBox1'])      
            if 'newCheckBox2' in request.POST:
                extras.append(request.POST['newCheckBox2']) 
            if 'newCheckBox3' in request.POST:
                extras.append(request.POST['newCheckBox3'])  
            sub_name = info[6:info.find(')')]
            if '#' in info:
                price = round(float(info[info.find('#') + 1:]), 2)
            else:
                price = round(float(info[info.find(')') + 1:]), 2) 
            extras_string = ""
            if len(extras) > 0:
                for extra in extras:
                    if extras.index(extra) != len(extras)-1:
                        extras_string += str(extra) + ' ,'
                    else:
                        extras_string += str(extra) + '. '
            else:
                extras_string += "No extras selected"
            o = Cart(user_id=request.user.id, order_contents=sub_name + "(" + size + ") " + "Extras (" + extras_string + " )", total_price = price, user_name = request.user)  
            o.save()  
            extras_string = ""                                             
            return HttpResponseRedirect(reverse("main_app"))     
    else: 
        all_carts = Cart.objects.filter(user_id__contains=request.user.id) 
        ttl = 0.00      
        cart_length = len(all_carts)
        for cart in all_carts:
            ttl += round(float(cart.total_price), 2)
        ttl = round(ttl,2)    
        cart_context = {"carts": all_carts, "total": ttl, "len" : cart_length}  
        return render(request, "orders/cart.html", cart_context)

@csrf_exempt
def main_app(request):  
    if request.method == "POST":
        info = request.POST["info"]
        u_place = info.find('_')
        size = info[:u_place] 
        t_name = info[u_place+1: u_place +6]   
        i_id = info[u_place+6:]
        if t_name == "Pizza":
            pizza= Pizza.objects.get(id=int(i_id))        
            if pizza.toppings_no > 0:
                toppings = pizza.toppings.all()
                reqd = list()
                for topping in toppings:
                    data = serializers.serialize('json', [ topping, ])
                    struct = json.loads(data)
                    data = json.dumps(struct[0])
                    Dict = eval(data)
                    reqd.append(Dict['fields']['name'])  
                if size == "small":
                    context_toppings = {"toppings_no": pizza.toppings_no, "toppings":reqd, "price": pizza.small_price, 'n' : pizza.toppings_no, "pizza": True, "size": "small", "name":pizza.name}
                    return JsonResponse(context_toppings)
                else:
                    context_toppings = {"toppings_no": pizza.toppings_no, "toppings":reqd, "price":pizza.large_price, 'n' : pizza.toppings_no, "pizza": True, "size": "large", "name":pizza.name}
                    return JsonResponse(context_toppings)
            else:
                if size == "large":
                    context_toppings = {"toppings_no": pizza.toppings_no, "price":pizza.large_price, "pizza": True, "size": "large", "name":pizza.name}
                    return JsonResponse(context_toppings)
                else:
                    context_toppings = {"toppings_no": pizza.toppings_no, "price":pizza.small_price, "pizza": True, "size": "small", "name":pizza.name}
                    return JsonResponse(context_toppings)
        elif "Dinner" in info:
            u_place = info.find('_')
            size = info[:u_place]
            i_id = info[u_place + 7:]
            dinner = Dinner.objects.get(id=int(i_id))         
            if size == "small":
                context_dinner = {"name": dinner.name, "price": dinner.small_price, "size": "small", "dinner": True}   
                return JsonResponse(context_dinner)
            else:
                context_dinner = {"name": dinner.name, "price": dinner.large_price, "size": "large", "dinner": True}
                return JsonResponse(context_dinner)
        elif "salad" in info:
            u_place = info.find('_')
            i_id = info[u_place+1:]
            salad = Salad.objects.get(id=int(i_id))
            context_salad = {"name": salad.name, "price": salad.price, "salad": True}
            return JsonResponse(context_salad)
        elif 'pasta' in info:
            u_place = info.find('_')
            i_id = info[u_place+1:]
            pasta = Pasta.objects.get(id=int(i_id))
            context_pasta = {"name": pasta.name, "price": pasta.price, "pasta": True}
            return JsonResponse(context_pasta)
        elif 'Sub' in info:
            u_place = info.find('_')
            size = info[:u_place] 
            i_id = info[u_place + 4:]
            sub = Sub.objects.get(id=int(i_id))
            toppings = sub.toppings.all()
            reqd = list()
            for topping in toppings:
                data = serializers.serialize('json', [ topping, ])
                struct = json.loads(data)
                data = json.dumps(struct[0])
                Dict = eval(data)
                reqd.append(Dict['fields']['name'])
            if size == "small":
                context_toppings_sub = {"toppings_no": sub.toppings_no, "toppings":reqd, "price": sub.small_price, 'n' : sub.toppings_no, "sub": True, "size": "small", "name":sub.name}
                return JsonResponse(context_toppings_sub)
            else:
                context_toppings_sub = {"toppings_no": sub.toppings_no, "toppings":reqd, "price": sub.large_price, 'n' : sub.toppings_no, "sub": True, "size": "large", "name":sub.name}
                return JsonResponse(context_toppings_sub)

    else:            
        if request.user.is_authenticated:
            pizzas = Pizza.objects.all()
            dinners = Dinner.objects.all()
            salads = Salad.objects.all()
            pastas = Pasta.objects.all()
            subs = Sub.objects.all()
            all_carts = Cart.objects.filter(user_id__contains=request.user.id) 
            cart_length = len(all_carts)
            context ={'pizzas': pizzas, "dinners": dinners, "salads":salads, "pastas": pastas, "subs": subs, "len": cart_length}
            return render(request, "orders/main.html", context)      
        else:
            return HttpResponseRedirect(reverse("index"))

def login(request):
    if request.method == "POST":
        username = request.POST['l_username']
        password = request.POST['l_password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("main_app"))
        else:
            messages.info(request, "invalid credentials")
            return HttpResponseRedirect(reverse("index"))
    else:           
        return HttpResponseRedirect(reverse("index")) 

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))

