
from django.shortcuts import redirect, render
from .models import Dragon, Rider
from django.contrib import messages
from django.db.models import Count
import bcrypt

# Create your views here.
#localhost:8000
def index(request):
    return render(request,"index.html")

def register_rider(request):
    if request.method == 'POST':
        errors = Rider.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')
        else:
            password=request.POST['password']
            salted_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_rider = Rider.objects.create(name=request.POST['name'], guild=request.POST['guild'], is_trained=request.POST['is_trained'] ,email=request.POST['email'], password=salted_pass)
            request.session['rider_id'] = new_rider.id
            return redirect("/dragons")
    return redirect('/')

def login_rider(request):
    rider = Rider.objects.filter(email=request.POST['email']) 
    if rider: 
        logged_rider = rider[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_rider.password.encode()):
            request.session['rider_id'] = logged_rider.id
            return redirect('/dragons')
    return redirect("/")

#localhost:8000/dragons
def show_dragons(request):
    if 'rider_id' not in request.session:
        return redirect("/")
        # Dragon.objects.annotate(likes=Count('riders_that_like_me')).order_by('likes') 
    ordered_dragons = Dragon.objects.annotate(likes=Count('riders_that_like_me')).order_by('-likes')
    context = {
        "all_dragons": ordered_dragons,
        "rider":Rider.objects.get(id=request.session['rider_id']),
    }
    return render(request,"show_dragons.html", context)

#localhost:8000/dragons/new
def new_dragons(request):
    if 'rider_id' not in request.session:
        return redirect("/")
    context = {
        "rider":Rider.objects.get(id=request.session['rider_id'])
    }
    return render(request,"new_dragons.html", context)

#localhost:8000/dragons/create
def create_dragons(request):
    if 'rider_id' not in request.session:
        return redirect("/")
    if request.method == 'POST': 
        errors = Dragon.objects.dragon_creator_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for value in errors.values():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/dragons/new')
        else:
            # if the errors object is empty, that means there were no errors!
            # retrieve the blog to be updated, make the changes, and save
            #create dragon
            Dragon.objects.create(name=request.POST['name'] , num_of_wings=request.POST['num_of_wings'] , has_magic=request.POST['has_magic'], my_rider=Rider.objects.get(id=request.POST['rider_id']))
            return redirect("/dragons")
    return redirect('/dragons/new')

def show_one_dragon(request, dragon_id):
    if 'rider_id' not in request.session:
        return redirect("/")
    context = {
        "dragon":Dragon.objects.get(id=dragon_id)
    }
    return render(request, "show_one_dragon.html", context)
    
#localhost:8000/dragons/{id}/edit
def edit_dragons(request, dragon_id):
    if 'rider_id' not in request.session:
        return redirect("/")
    logged_user = Rider.objects.get(id=request.session['rider_id'])
    dragon_to_edit = Dragon.objects.get(id=dragon_id)
    if logged_user.id != dragon_to_edit.my_rider.id:
        return redirect("/dragons")
    context = {
        "dragon":dragon_to_edit,
        "all_riders":Rider.objects.all(),
    }
    return render(request,"edit_dragons.html", context)

#localhost:8000/dragons/{id}/update
def update_dragons(request, dragon_id):
    if 'rider_id' not in request.session:
        return redirect("/")
    if request.method == 'POST':
        errors = Dragon.objects.dragon_creator_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for value in errors.values():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect(f'/dragons/{dragon_id}/edit')
        else:
            # if the errors object is empty, that means there were no errors!
            # retrieve the blog to be updated, make the changes, and save
            #create dragon
            thisDragon = Dragon.objects.get(id=dragon_id)
            thisDragon.name = request.POST['name']
            thisDragon.num_of_wings = request.POST['num_of_wings']
            thisDragon.has_magic = request.POST['has_magic']
            thisDragon.save()
            return redirect(f"/dragons/{dragon_id}")
    return redirect(f'/dragons/{dragon_id}/edit')

#localhost:8000/dragons/like
def like_dragons(request, dragon_id):
    if 'rider_id' not in request.session:
        return redirect("/")
    #need a rider
    rider = Rider.objects.get(id=request.session['rider_id'])
    #need a dragon
    dragon = Dragon.objects.get(id=dragon_id)
    #get dragons list of riders who like
    liking_riders = dragon.riders_that_like_me
    #add rider to list of riders
    liking_riders.add(rider)
    return redirect("/dragons")

def unlike_dragons(request, dragon_id):
    if 'rider_id' not in request.session:
        return redirect("/")
    #need a rider
    rider = Rider.objects.get(id=request.session['rider_id'])
    #need a dragon
    dragon = Dragon.objects.get(id=dragon_id)
    #get dragons list of riders who like
    liking_riders = dragon.riders_that_like_me
    #add rider to list of riders
    liking_riders.remove(rider)
    return redirect("/dragons")


def destroy(request, dragon_id):
    if 'rider_id' not in request.session:
        return redirect("/")
    if request.method == "POST":
        logged_user = Rider.objects.get(id=request.session['rider_id'])
        dragon_to_delete = Dragon.objects.get(id=dragon_id)
        if logged_user.id == dragon_to_delete.my_rider.id:
            dragon_to_delete.delete()
        else:
            return redirect("/dragons")
    return redirect("/dragons")

def logout(request):
    request.session.flush()
    return redirect('/')