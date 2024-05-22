from django.contrib import admin
from .models import Category, Post, Turf_multi_image, Location,Turf, Slots, Booking, Profile, TurfCategory, Feedback,Userblock, Contact,RatingDB

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Turf_multi_image)
admin.site.register(Location)
admin.site.register(Turf)
admin.site.register( Slots)
admin.site.register( Booking)
admin.site.register( Profile)
admin.site.register(TurfCategory)
admin.site.register(Feedback)
admin.site.register(Contact)
admin.site.register(RatingDB)

class UserblockAdmin(admin.ModelAdmin):
    list_display = ('user', 'block_status',)
    fields = ('user', 'block_status')

admin.site.register(Userblock,UserblockAdmin)