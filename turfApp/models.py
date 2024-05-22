from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    description = models.TextField()
    description2 = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Add default=None
    img = models.ImageField(upload_to="uploads/images" ,null=True,blank=True)
    # admin_whtsappnumber= models.IntegerField(default=0, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return self.title  

class Contact(models.Model):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.phone_number}, {self.address}, {self.email}"

class Location(models.Model):
    name = models.CharField(max_length=255) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  

class TurfCategory(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to="uploads/images" ,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name


class Turf(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True)
    turfcategory=models.ForeignKey(TurfCategory, on_delete=models.CASCADE ,  default=1)
    img = models.ImageField(upload_to="uploads/images" ,null=True,blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)  # Add default=None
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement_image =  models.ImageField(upload_to="uploads/images" ,null=True,blank=True)

    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name      
    
class Turf_multi_image(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, null=True, default=None)
    img = models.FileField(upload_to="uploads/images" ,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Turf {self.turf}"


class Slots(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    times=models.TimeField()

    def formatted_time(self):
        return self.times.strftime("%H:%M")

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add default=None
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slots, on_delete=models.CASCADE)
    no_of_players = models.PositiveIntegerField()
    date= models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    no_of_booking=models.IntegerField(default=1)
    phonenumber=models.CharField(max_length=10)
    booking_status = models.IntegerField(choices=[(1, 'Active'), (0, 'Canceled')], default=1)

    def cancel_booking(self):
        self.booking_status = 0
        self.save()

    def __str__(self):
        return f"Booking by {self.user} for {self.no_of_players} players at {self.turf} in slot {self.slot}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.FileField(upload_to="uploads/images" ,null=True,blank=True)
    name = models.CharField(max_length=255)
    address = models.TextField(max_length=500, blank=True)
    place = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    
    roll = models.CharField(max_length=7, choices=[('user', 'user'), ('owner', 'owner')], default='user')


class Feedback(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)  # Define an 'email' field for the email address
    feedback = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name  # Customize the string representation as needed


# class AdminContact(models.Model):
#     whatsapp_number = models.IntegerField(default=0)

#     def __str__(self):
#         return str(self.whatsapp_number)



# class User(models.Model):
#     username = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     email = models.EmailField()  
#     address = models.TextField()
#     place = models.CharField(max_length=255)  
#     countrty = models.CharField(max_length=255)  
#     district= models.CharField(max_length=255)
#     img = models.ImageField(upload_to="uploads/images" ,null=True,blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
 
#     def __str__(self):
#         return self.name  

class Userblock(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    block_status = models.BooleanField(default=True)
    


class RatingDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, null=True)

    Rating = models.IntegerField(blank=True,null=True)
   

class Meta:
        unique_together = ('user', 'turf')  
