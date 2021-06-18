from django.db import models
import re

# Create your models here.

class RiderManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        
        if len(postData['name']) < 2:
            errors['name'] = "Hey, name has to be at least 2 characters"
        if len(postData['guild']) < 4:
            errors['guild'] = "Hey, name has to be at least 4 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long, yo."
        if postData['password'] != postData['password_confirm']:
            errors['pass_conf'] = "Passwords must match. Duh!"
        email_to_create = Rider.objects.filter(email=postData['email'])
        if email_to_create:
            errors['unique'] = "Email already in use."
        
        return errors

class DragonManager(models.Manager):
    def dragon_creator_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Hey, name has to be at least 2 characters"
        if len(postData['num_of_wings']) == 0:
            errors['num_of_wings'] = "Hey, Number of Wings has to be at least 1 number"
        return errors

class Rider(models.Model):
    name = models.CharField(max_length=17)
    guild = models.CharField(max_length=15)
    email = models.TextField()
    password = models.TextField()
    is_trained = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #my_dragons
    #dragons_liked
    objects = RiderManager()

class Dragon(models.Model):
    #id
    name = models.CharField(max_length = 17)
    num_of_wings = models.IntegerField()
    has_magic = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_rider = models.ForeignKey(Rider, related_name="my_dragons", on_delete = models.CASCADE)
    riders_that_like_me = models.ManyToManyField(Rider, related_name="dragons_liked")
    objects = DragonManager()
    