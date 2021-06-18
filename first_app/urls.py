from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #logreg form
    path('register', views.register_rider), #back-end registration functionality
    path('login', views.login_rider), #back-end login functionality
    #website starts here
    path('dragons', views.show_dragons), #localhost8000/dragons
    path('dragons/new', views.new_dragons), #localhost8000/dragons/new
    path('dragons/create', views.create_dragons), #localhost8000/dragons/create
    path('dragons/<int:dragon_id>', views.show_one_dragon), #localhost8000/dragons/1
    path('dragons/<int:dragon_id>/edit', views.edit_dragons), #localhost8000/dragons/1/edit
    path('dragons/<int:dragon_id>/update', views.update_dragons), #localhost8000/dragons/1/update
    path('dragons/<int:dragon_id>/like', views.like_dragons), #localhost8000/dragons/1/like
    path('dragons/<int:dragon_id>/unlike', views.unlike_dragons), #localhost8000/dragons/1/unlike
    path('dragons/<int:dragon_id>/destroy', views.destroy), #localhost8000/dragons/1/destroy
    #logout
    path('dragons/logout', views.logout), #localhost8000/dragons/logout
]
