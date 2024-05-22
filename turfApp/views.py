from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Post, TurfCategory, Turf, Location, Turf_multi_image, Slots,Booking, Feedback, Contact
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import re
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile  # Import your profile model
from .forms import MultipleImageUploadForm
from django.contrib.auth import logout
User = get_user_model()
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from .models import Userblock  


def base(request):
    ids=request.user.id
    roll=Profile.objects.filter(user_id=ids).values_list('roll',flat=True)
    return render(request,'layout.html',{'roll':roll})



def index(request):
    user_id = request.user.id
    roll = get_user_role(user_id)
    
    dict_index = {
        'slider': Post.objects.filter(category_id=1),
        'Categories_home_page': Post.objects.filter(category_id=2),
        'Featured_Product': Post.objects.filter(category_id=3),
        'categories': TurfCategory.objects.all(),
        'featured_product': Turf.objects.all(),
        'roll': roll
    }

    return render(request, 'index.html', dict_index)

def get_user_role(user_id):
    try:
        return Profile.objects.filter(user_id=user_id).values_list('roll', flat=True).first()
    except Profile.DoesNotExist:
        return None
  

def about(request):
    dict_about={

        'about' :Post.objects.filter(category_id=4),
        'Our_Services' :Post.objects.filter(category_id=5),
        'Our_Brands' :Post.objects.filter(category_id=6),
        'aboutpage_banner' : Post.objects.filter(category_id=8)
    }
    return render(request,'about.html',dict_about)

def turf(request, turf_id):
    turf_object = get_object_or_404(Turf, id=turf_id)
    user = request.user
    roll = get_user_role(user.id)  # Assuming you have a get_user_role function

    context = {
        'turf_object': turf_object,
        'roll': roll
    }

    return render(request, 'turf.html', context)

# def contact(request,turf_id):
    
#     return render(request,'contact.html')

def user_register(request):
    if request.method == 'POST':
        image=request.FILES.get('image',None)
        name = request.POST.get('name')
        username = request.POST.get('username')
        # password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        place = request.POST.get('place')
        district = request.POST.get('district')
        country = request.POST.get('country')
        user_role = request.POST.get('role')
        

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Username or email is already in use.'}, status=400)

        new_password = request.POST.get('password')  # Get the new password from the form

        if len(new_password) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters long.'}, status=400)
        elif not re.search(r'\d', new_password):
            return JsonResponse({'error': 'Password must contain at least one number.'}, status=400)
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            return JsonResponse({'error': 'Password must contain at least one special character.'}, status=400)

        # Create the user
        user = User(username=username, email=email)
        user.set_password(new_password)  # Set the new password
        user.save()

        profile = Profile(user=user, img=image, name=name, address=address, place=place, district=district, country=country, roll= user_role)
        profile.save()

        # # Log the user in after registration (optional)
        # login(request, user)
        # After saving the user, authenticate the user and then log them in.
        user = authenticate(request, username=username, password=new_password)
        if user is not None:
  # Redirect to the login page
            return JsonResponse({'message': 'User registered and logged in successfully','redirect':'/login_page'})
        else:
            return JsonResponse({'error': 'User authentication failed'}, status=400)

        # return JsonResponse({'message': 'User registered successfully'})
        # You can also consider redirecting to the login page here if needed.

    return render(request, 'user_register.html')    
   

# def user_register(request):
#     if request.method == 'POST':
#             name = request.POST.get('name')
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             email = request.POST.get('email')
#             address = request.POST.get('address')
#             place = request.POST.get('place')
#             district = request.POST.get('district')
#             country = request.POST.get('country')

#             if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#                 return JsonResponse({'error': 'Username or email is already in use.'}, status=400)

#             #Create the user
#             user = User(username=username, email=email)
#             user.set_password(password)
#             user.save()

#             # new_password = "password"  # Replace 'new_password_here' with the new password you want to set.

#             # if len(new_password) < 8:
#             #      print("Password must be at least 8 characters long.")
#             # elif not re.search(r'\d', new_password):
#             #     print("Password must contain at least one number.")
#             # elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
#             #     print("Password must contain at least one special character.")
#             # else:
#             #     user = User(username=username, email=email)
#             #     # If the password meets all the requirements, set it for the user.
#             #     user.set_password(new_password)
#             #     user.save()
#             #     print("Password changed successfully.")




#             profile = Profile(user=user,name=name, address=address, place=place, district=district, country=country)
#             profile.save()
#             print("User registered successfully.")
#             return JsonResponse({'message': 'User registered successfully'})
#             # return redirect('login')
        
#     return render(request, 'user_register.html')    



def login_page(request):
    
    
    return render(request,'login.html')

# def success_login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         try:
#             user=authenticate(username=username,password=password)
#             login(request, user)
#             return JsonResponse({'success': True, 'message': 'Login successful', 'redirect': '/myprofile'})
           

#         except User.DoesNotExist :
#             # Handle case where user is not found (authentication fails)
#             return JsonResponse({'error':'Invalid credentials. email or password is incorrect.'})
    
def success_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User authentication successful
                block_status = Userblock.objects.filter(user=user).values_list('block_status', flat=True).first()

                if block_status is None:
                    login(request, user)
                    return JsonResponse({'success': True, 'message': 'Login successful', 'redirect': '/myprofile'})
                elif block_status:
                    return JsonResponse({'success': False, 'message': 'your blocked contact admin.'})
                else:
                    login(request, user)
                    return JsonResponse({'success': True, 'message': 'Login successful', 'redirect': '/myprofile'})
            else:
                # User authentication failed
                return JsonResponse({'success': False, 'message': 'Invalid credentials. Email or password is incorrect.'})
        except User.DoesNotExist:
            # Handle case where user is not found (authentication fails)
            return HttpResponse("Invalid credentials. Email or password is incorrect.")
        


# def turf_singlepage(request,turf_id):

#     # # Retrieve the specific turf using the turf_id (assuming you pass it in the URL)
#     # turf = Turf.objects.all()

#     # # Retrieve multiple images associated with the turf
#     # images = Turf_multi_image.objects.filter(turf=turf)

#     dict_turfsinglepage={
#          'turf' : get_object_or_404(Turf, id=turf_id),
#         # 'turf_category' : Turf.objects.get(pk=turf_id),
#          'multi_image': Turf_multi_image.objects.filter(turf=turf_id)
#         # 'turf': turf,
#         # 'images': images,

#     }
     
#     return render(request, 'turf-singlepage.html',dict_turfsinglepage)       

def turf_singlepage(request, turf_id):
    # Retrieve the specific turf using the turf_id
    turf = get_object_or_404(Turf, id=turf_id)

    # Get the user and user's role
    user = request.user
    roll = get_user_role(user.id)  # Assuming you have a get_user_role function

    # Get the turf's category
    turfcategory_id = turf.turfcategory.id

    # Retrieve multiple images associated with the turf
    multi_image = Turf_multi_image.objects.filter(turf=turf_id)

    # Query the related products excluding the current turf
    related_turf = Turf.objects.filter(turfcategory_id=turfcategory_id).exclude(id=turf_id)

    dict_turfsinglepage = {
        'turf': turf,
        'multi_image': multi_image,
        'related_turf': related_turf,
        'roll': roll  # Add user's role to the context
    }

    return render(request, 'turf-singlepage.html', dict_turfsinglepage)


# def related_products(request, turfcategory_id):
#     # Query the related products based on some criteria (e.g., category, tags, etc.)
#     related_turf = Turf.objects.filter(turfcategory_id=turfcategory_id)  # Adjust your filter criteria

#     context = {
#         'related_turf': related_turf
#     }

#     return render(request, 'turf-singlepage.html', context)    


def turf_booking(request,turf_id):

    turfid= turf_id
    today = timezone.now().date()
    upcoming_bookings = Booking.objects.filter(date__gte=today)
     
    dict_booking={
        'booking' :Slots.objects.all(),
        'turfid' :turfid,
        'upcoming_bookings': upcoming_bookings,
    }
      
    return render(request,'turf-booking.html',dict_booking)   
    
   
    

# from datetime import datetime, timedelta
# def turf_booking_save(request):
#     user_id = request.user.id

#     if request.method == 'POST':
#         no_of_players = request.POST.get('numberofplayers')
#         date = request.POST.get('date')
#         slot_id = request.POST.get('slots')
#         today = timezone.now().time()
#         time_slot = Slots.objects.filter(id=slot_id).values_list('times', flat=True).first()
        
#         # Convert time_slot to timezone-aware datetime
#         time_slot = timezone.make_aware(datetime.combine(datetime.today(), time_slot))
        
#         turf_id = request.POST.get('turf_id')
#         date_object = datetime.strptime(date, "%Y-%m-%d")
#         date_only = date_object.date()
#         time_only = date_object.time()
#         now = timezone.now()
#         today = timezone.now().date()
#         if date_only == today:
#          if now > time_slot:
#             return JsonResponse({'error': 'Cannot book in past time'})
#         else:
#             pass
#         if date_only < today:
#             return JsonResponse({'error': 'Cannot book for past dates'})

#         if not all([no_of_players, date, slot_id]):
#             return JsonResponse({'error': 'All fields are required'})

#         # Check availability for the selected slot on the specified date
#         existing_booking = Booking.objects.filter(date=date_only, slot_id=slot_id, turf_id=turf_id).first()

#         if existing_booking:
#             if existing_booking.booking_status == 0:
#                 # Allow booking for canceled slots
#                 existing_booking.booking_status = 1
#                 existing_booking.save()
#             else:
#                 return JsonResponse({'error': 'Slot is already booked for the selected date and time'})

#         else:
#             # If no existing booking, create a new one
#             booking = Booking(no_of_players=no_of_players, date=date_only, slot_id=slot_id, user_id=user_id, turf_id=turf_id)
#             booking.save()

#         return JsonResponse({'message': 'Turf booked successfully'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from .models import Booking, Slots

from django.utils import timezone

from django.utils import timezone

# def turf_booking_save(request):
#     user_id = request.user.id

#     if request.method == 'POST':
#         no_of_players = request.POST.get('numberofplayers')
#         date = request.POST.get('date')
#         slot_id = request.POST.get('slots')
#         today = timezone.now().time()
#         time_slot = Slots.objects.filter(id=slot_id).values_list('times', flat=True).first()
        
#         # Convert time_slot to timezone-aware datetime
#         time_slot = timezone.make_aware(datetime.combine(datetime.today(), time_slot))
#         timeslot=time_slot.time()
#         print(timeslot)
        
#         turf_id = request.POST.get('turf_id')
#         date_object = datetime.strptime(date, "%Y-%m-%d")
#         date_only = date_object.date()
#         print(date_only)
#         time_only = date_object.time()
#         now = timezone.now()
#         time_now = timezone.now().time()
#         print(time_now)
#         today = timezone.now().date()
#         if date_only == today:
#          if time_now > timeslot:
#             return JsonResponse({'error': 'Cannot book in past time'})
#          else:
#             print('not today')
#         if date_only < today:
#             return JsonResponse({'error': 'Cannot book for past dates'})

#         if not all([no_of_players, date, slot_id]):
#             return JsonResponse({'error': 'All fields are required'})

#         # Check availability for the selected slot on the specified date
#         existing_booking = Booking.objects.filter(date=date_only, slot_id=slot_id, turf_id=turf_id).first()


#         # Validate phone number
#         phonenumber = request.POST.get('phonenumber')
#         if not phonenumber or not phonenumber.isdigit() or len(phonenumber) != 10:
#             return JsonResponse({'error': 'Invalid phone number. Please enter a 10-digit number.'})

#         # Check availability for the selected slot on the specified date
#         existing_booking = Booking.objects.filter(date=date_only, slot_id=slot_id, turf_id=turf_id).first()

#         if existing_booking:
#             if existing_booking.booking_status == 0:
#                 # Allow booking for canceled slots
#                 existing_booking.booking_status = 1
#                 existing_booking.save()
#             else:
#                 return JsonResponse({'error': 'Slot is already booked for the selected date and time'})

#         else:
#             # If no existing booking, create a new one
#             booking = Booking(
#                 no_of_players=no_of_players,
#                 date=date_only,
#                 slot_id=slot_id,
#                 user_id=user_id,
#                 turf_id=turf_id,
#                 phonenumber=phonenumber  # Add the phone number to the Booking model if you have a field for it
#             )
#             booking.save()

#         return JsonResponse({'message': 'Turf booked successfully'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})


def turf_booking_save(request):
    user_id = request.user.id

    if request.method == 'POST':
        no_of_players = request.POST.get('numberofplayers')
        date = request.POST.get('date')
        slot_id = request.POST.get('slots')
        today = timezone.now().time()
        time_slot = Slots.objects.filter(id=slot_id).values_list('times', flat=True).first()
        time_zone1 = timezone.get_current_timezone()

        time_now= timezone.now().astimezone(time_zone1).time()
        print("time:", time_now)

        
        # Convert time_slot to timezone-aware datetime
        time_slot = timezone.make_aware(datetime.combine(datetime.today(), time_slot))
        timeslot=time_slot.time()
        print('hit',timeslot)
        
        turf_id = request.POST.get('turf_id')
        date_object = datetime.strptime(date, "%Y-%m-%d")
        date_only = date_object.date()
        print(date_only)

        print(time_now)
        today = timezone.now().date()
        if date_only == today:
         if time_now > timeslot:
            return JsonResponse({'error': 'Cannot book in past time'})
         else:
            print('not today')
        if date_only < today:
            return JsonResponse({'error': 'Cannot book for past dates'})

        if not all([no_of_players, date, slot_id]):
            return JsonResponse({'error': 'All fields are required'})

        # Check availability for the selected slot on the specified date
        existing_booking = Booking.objects.filter(date=date_only, slot_id=slot_id, turf_id=turf_id).first()


        # Validate phone number
        phonenumber = request.POST.get('phonenumber')
        if not phonenumber or not phonenumber.isdigit() or len(phonenumber) != 10:
            return JsonResponse({'error': 'Invalid phone number. Please enter a 10-digit number.'})

        # Check availability for the selected slot on the specified date
        existing_booking = Booking.objects.filter(date=date_only, slot_id=slot_id, turf_id=turf_id).first()

        if existing_booking:
            if existing_booking.booking_status == 0:
                # Allow booking for canceled slots
                existing_booking.booking_status = 1
                existing_booking.save()
            else:
                return JsonResponse({'error': 'Slot is already booked for the selected date and time'})

        else:
            # If no existing booking, create a new one
            booking = Booking(
                no_of_players=no_of_players,
                date=date_only,
                slot_id=slot_id,
                user_id=user_id,
                turf_id=turf_id,
                phonenumber=phonenumber  # Add the phone number to the Booking model if you have a field for it
            )
            booking.save()

        return JsonResponse({'message': 'Turf booked successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def myprofile(request):
    ids = request.user.id
    roll = Profile.objects.filter(user_id=ids).values_list('roll', flat=True).first()
    print(roll)

    try:
        log_det2 = Profile.objects.get(user_id=ids)
        turfs = Turf.objects.filter(user=request.user)  # Fix: Use request.user instead of undefined user
        data = {
            'log_det1': request.user,
            'log_det2': log_det2,
            'roll': roll,
            'turfs': turfs
        }
    except:
        return HttpResponse('Sorry, you are not logged in')  # Fix: Return a response on error

    return render(request, 'profile.html', data)
# def profile(request):
#     if 'session1' in request.session:
#         ids = request.session.get('session1', None)
#         if ids is not None:
#             try:
#                 user = User.objects.get(id=ids)
#                 profile = Profile.objects.get(user_id=ids)
#                 data = {
#                     'log_det1': user,
#                     'log_det2': profile
#                 }
#                 return render(request, 'profile.html', data)
#             except User.DoesNotExist:
#                 # Handle the case where the user does not exist
#                 return HttpResponse('User not found')
#             except Profile.DoesNotExist:
#                 # Handle the case where the profile does not exist
#                 return HttpResponse('Profile not found')
#         else:
#             # Handle the case where 'session1' is None
#             return HttpResponse('Invalid session data')
#     else:
#         # Handle the case where 'session1' is not in session data
#         return HttpResponse('Sorry, you are not logged in. Login to create a profile')

def edit(request):
        ids = request.user.id
        log_det1 = User.objects.get(id=ids)
        log_det2=Profile.objects.get(user_id=ids)
        data={
            'log_det1':log_det1,
            'log_det2':log_det2
        }
        return render(request,'edit.html',data)

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Profile  # Make sure to import your Profile model

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Profile

def edit_save(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        place = request.POST.get('place')
        district = request.POST.get('district')
        country = request.POST.get('country')

        ids = request.user.id
        profile = Profile.objects.get(user_id=ids)
        user = profile.user

        # Check if the new username is the same as the existing one
        if user.username != username:
            # Check if the new username already exists in the database
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                # If the new username is different and already exists, return an error message
                return JsonResponse({'message': 'Username already exists'}, status=400)

            # If the new username is different and doesn't exist, update it
            user.username = username

        user.email = email
        user.save()

        # Update profile data, including the image
        if 'image' in request.FILES:
            profile.img = request.FILES['image']

        profile.name = name
        profile.address = address
        profile.place = place
        profile.country = country
        profile.district = district

        # Check if 'image' is present in request.FILES and it is not None before accessing it
        if 'image' in request.FILES and request.FILES['image'] is not None:
            profile.image = request.FILES['image']

        profile.save()

        return redirect('myprofile')

    return render(request, 'edit.html')



# def turf_list(request):
#     user_id = request.session.get('session1')
#     # turf_id = request.POST.get('turf_id')

#     # try:
#         # user = User.objects.get(user_id=user_id)
#         # turf = Turf.objects.get(turf_id=turf_id) if turf_id else None

#         # Retrieve a list of Turf objects created by the user
#     turf_list = Turf.objects.filter(id=user_id)

#     # context = {
#     #         # 'user': user,
#     #         # 'turf': turf,
#     #         'turf_list': turf_list
#     #     }

#     # except (User.DoesNotExist, Turf.DoesNotExist):
#     #     return render(request, 'turf_list.html', {'error_message': 'User or Turf not found'})

#     return render(request, 'turf_list.html')

def turf_list(request):
    user_id = request.user.id
    turf_list = Turf.objects.filter(user=user_id)
    idss=Turf.objects.filter(user=user_id).values_list('id',flat=True)
    idk=[]
    idt=[]
    for i in idss:
        iditem=Booking.objects.filter(turf_id=i).values_list('no_of_booking',flat=True)
        print(iditem)
        idts=sum(iditem)
        idt.append(idts)
        print(i,idt)
        idk.append(i)
    print(idk)
   
    # if request.method == 'POST':
    #     turf_ids = request.POST.getlist('turf_ids[]')
    #     booking_counts = {}
        
    #     for item_id in turf_ids:
    #         # Count the number of bookings for each turf
    #         booking_count = Booking.objects.filter(turf_id=item_id).count()
    #         booking_counts[item_id] = booking_count
            
    #     print(booking_count)
        
    #     # Pass the turf_list and booking_counts to the template
    #     return render(request, 'turf_list.html', {'turf_list': turf_list, 'booking_counts': booking_counts})
    
    return render(request, 'turf_list.html', {'turf_list': turf_list,'idt':idt,'idk':idk, 'user_id':user_id})

def view_bookings(request,turf_id):
    user_id = request.user.id
    turf = get_object_or_404(Turf, id=turf_id)
    # try:
    user = User.objects.get(id=user_id)  # Retrieve the User object by ID

    # Query the booking records for the user
    bookings = Booking.objects.filter(turf=turf)

    # except User.DoesNotExist:
        # Handle the case where the User doesn't exist
        # error_message = "The requested User does not exist."
        # return render(request, 'error_page.html', {'error_message': error_message})

    data = {
        'user': user,
        'turf' : turf,
        'bookings': bookings,
        'user_id':user_id,
    }


    return render(request, 'view-bookings.html', data) 

@login_required
def delete_turf(request):
    turf_id = request.POST.get('turf_id')
    try:

        turf = get_object_or_404(Turf, id=turf_id)
        turf.delete()
        return JsonResponse({'message': 'Turf deleted successfully.'})
    except:
        return JsonResponse({'error': 'You are not authorized to delete this turf.'}, status=403)       

# @login_required  # Ensure that only authenticated users can access this view
# def delete_turf(request, turf_id):
#     turf = get_object_or_404(Turf, id=turf_id)

#     # Check if the logged-in user is the owner of the turf
#     if request.user == turf.user:
#         turf.delete()
#         return redirect('turf_list')  # Redirect to a relevant page after deletion
#     else:
#         # Handle the case where the user is not the owner of the turf
#         # You may want to show an error message or redirect to an error page
#         return render(request, 'turf_list.html', {'error_message': 'You are not authorized to delete this turf.'})   

# def turf_list(request):
#     user_id = request.session.get('session1')
#     turf_id = request.POST.get('turf_id')
    
#     # if turf_id is None:
#     #     # Handle the case when turf_id is not found in the POST data
#     #     return render(request, 'turf_list.html', {'error_message': 'Turf ID is missing in the POST data'})
    
#     try:
#         user = User.objects.get(id=user_id)  # Assuming you have a User model
#         turf = Turf.objects.get(id=turf_id)
#         # Now, to retrieve a list of Turf objects, you can use a query like this:
#         turf_list = Turf.objects.all()  # This retrieves all Turf objects
#         # You can filter the Turf objects based on your specific criteria if needed, like filtering by user or other attributes.
#         # turf_list = Turf.objects.filter(some_field=some_value)

#         list = {
#             'user': user,
#             'turf': turf,
#             # 'turf_list': turf_list  # Pass the list of Turf objects to the template
#         }
   
#     except (User.DoesNotExist, Profile.DoesNotExist, Booking.DoesNotExist, Turf.DoesNotExist):
#         return render(request, 'turf_list.html', {'error_message': 'User, Profile, Booking, or Turf not found'})
    
#     return render(request, 'turf_list.html', list)
    
    # return render(request,'turf_list.html')
    # name = Turf.objects.get()
    # address=Turf.objects.get(address=address)
    # image = Turf.objects.get(img=image)
    # amount = Turf.objects.get(amount=amount)
    # dict_list={
    #     'name' : name,
    #     'address' : address,
    #     ' image' : image,
    #     ' amount' : amount,

    # }
    # turf = Turf.objects.get(id=turf_id)  # Retrieve the Turf object by its ID
    # context = {'turf': turf}
    # try:
    #     turf = Turf.objects.get(id=turf_id)  # Retrieve the Turf object by its ID
    # except Turf.DoesNotExist:
    #     # Handle the case where the turf doesn't exist
    #     turf = None


    # context = {'turf': turf}


    # return render(request,'turf_list.html', list)  



def change_password(request):

    return render(request,'change_password.html')

def success_changepassword(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Custom password complexity validation
        errors = []
        if len(new_password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in new_password):
            errors.append('Password must contain at least one number.')
        if not any(char in "!@#$%^&*()_+[]{};:,.<>" for char in new_password):
            errors.append('Password must contain at least one special character.')

        if errors:
            return JsonResponse({'errors': errors})

        # Check if the current password matches the user's actual password
        if not request.user.check_password(current_password):
            return JsonResponse({'errors': ['Current password is incorrect.']})
        elif new_password != confirm_new_password:
            return JsonResponse({'errors': ['New password and confirmation do not match.']})
        else:
            # Update the user's password
            request.user.set_password(new_password)
            request.user.save()
            # Update the session to keep the user logged in
            update_session_auth_hash(request, request.user)
            return JsonResponse({'message': 'Password changed successfully.'})


def notification(request):
    user_id = request.user.id
    turf_id = 1
    
    try:
        user = User.objects.get(id=user_id)
        turf = Turf.objects.get(id=turf_id)
        # profile = Profile.objects.get(user_id=user_id)
        # booking = Booking.objects.filter(user_id=user_id)
        # slot= Slots.objects.get(id=slot_id)
        data = {
            'user': user,
            'turf': turf,
            # 'profile': profile,
            # 'booking': booking,
            # 'slot' : slot
        }
    except (User.DoesNotExist, Turf.DoesNotExist, Profile.DoesNotExist, Booking.DoesNotExist):
        return render(request, 'notification.html', {'error_message': 'User, Turf, Profile, or Booking not found'})


        # data = {
        #     'user': user,
        #     'profile': profile,
        #     'booking': booking,
        # }

    return render(request, 'notification.html', data)


# def notification_details(request):
    #  if 'session1' in request.session:
    #     ids = request.session.get('session1')
        
            
                # profile = Profile.objects.get(id=ids)
                # booking=Booking.objects.get(user_id=ids)
                # data={
                #     'profile':profile,
                #     'booking':booking
                # }
                # return render(request, data)
def user_notification(request):
    user_id = request.user.id
    
    # try:
    user = User.objects.get(id=user_id)  # Retrieve the User object by ID

    # Query the booking records for the user
    bookings = Booking.objects.filter(user_id=user_id)

    # except User.DoesNotExist:
        # Handle the case where the User doesn't exist
        # error_message = "The requested User does not exist."
        # return render(request, 'error_page.html', {'error_message': error_message})

    data = {
        'user': user,
        'bookings': bookings,
    }

    return render(request, 'user_notification.html', data)

# def cancel_booking(request):
#     try:
#         # Get the booking ID from the POST request
#         booking_id = request.POST.get('booking_id')
#         turf_id = request.POST.get('turf_id')

#         # Check if the booking exists based on both ID and turf
#         booking = Booking.objects.get(id=booking_id, turf_id=turf_id)

#         # Here, you can add any additional checks, e.g., user authorization, time constraints, etc.

#         # Cancel the booking (you may need to implement a method to do this in your model)
#         booking.cancel()

#         # Return a success message
#         return JsonResponse({'message': 'Booking cancelled successfully'})
#     except Booking.DoesNotExist:
#         # Handle the case where the booking doesn't exist
#         return JsonResponse({'error': 'Booking does not exist'})
#     except Exception as e:
#         # Handle other errors or exceptions
#         return JsonResponse({'error': f'Failed to cancel the booking: {str(e)}'})
# def cancel_booking(request):
#     if request.method == 'POST':
#         booking_id = request.POST.get('booking_id')

#         try:
#             # Retrieve the booking
#             booking = Booking.objects.get(id=booking_id)

#             # Cancel the booking (you may need to implement a `cancel` method in your Booking model)
#             booking.cancel()

#             return JsonResponse({'message': 'Booking cancelled successfully'})
#         except Booking.DoesNotExist:
#             return JsonResponse({'error': 'Booking does not exist'})
#         except Exception as e:
#             return JsonResponse({'error': f'Failed to cancel the booking: {str(e)}'})

#     return JsonResponse({'error': 'Invalid request method'})

def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('bookingId')
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
        success_message = "Booking canceled successfully."
        response_data = {'status': 'success', 'message': success_message}
    else:
        success_message = "You don't have permission to cancel this booking."
        response_data = {'status': 'error', 'message': success_message}

    # Return a JSON response with the cancellation status
    return JsonResponse(response_data)


# def cancel_booking(request):
#     if request.method == 'POST':
#         booking_id = request.POST.get('bookingId')
#         booking = Booking.objects.get(id=booking_id)
#         booking.delete()
#         success_message = "Booking canceled successfully."
#         response_data = {'status': 'success', 'message': success_message}
#     else:
#         success_message = "You don't have permission to cancel this booking."
#         response_data = {'status': 'error', 'message': success_message}

#     # Return a JSON response with the cancellation status
#     return JsonResponse(response_data)

   
@login_required
def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('login_page')



# def search_turf(request):
#     if request.method == 'POST': 
#         all_turfs = Turf.objects.all() 
#         keyword = request.POST.get('keyword')  # Get the keyword parameter from the request

#         # Perform a database query to find turf based on the keyword
#         try:
#             turfs = Turf.objects.filter(name=keyword)
#             turflist = [{'image': turf.img.url, 'name': turf.name, 'description': turf.description, 'turf_id': turf.id} for turf in turfs]
#             return JsonResponse({"turflist": turflist})
      
#         except Turf.DoesNotExist:
#             # Handle the case where no turfs match the search criteria
#             return JsonResponse({"message": "Feedback submitted successfully."})
      
    
#     return render(request, 'turf.html')
from django.http import JsonResponse
from django.shortcuts import render
from .models import Turf

from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse
from .models import Turf
def search_turf(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        # Perform a case-insensitive partial match on Turf name and Location name
        turfs = Turf.objects.filter(name__icontains=keyword) | Turf.objects.filter(location__name__icontains=keyword)

        if turfs.exists():
            # Create a list of dictionaries containing turf information
            turflist = [{'image': turf.img.url, 'name': turf.name, 'description': turf.description, 'location': turf.location.name, 'turf_id': turf.id} for turf in turfs]
            print("Turflist:", turflist)  # Add this line for debugging
            return JsonResponse({"turflist": turflist})
        else:
            print("No turfs found")  # Add this line for debugging
            return JsonResponse({"turflist": []})
    # If the request method is not POST, render the turf.html template
    return render(request, 'turf.html')

from .models import RatingDB  # Replace with your actual model import


# def saverating(request, turf_id):
#     if request.method == "POST":
#         rating_value = request.POST.get('property_rating')

#         try:
#             turf = Turf.objects.get(id=turf_id)

            
            
#             # Get the currently logged-in user
#             user = request.user

#             # Validate and convert the rating value to an integer
#             try:
#                 rating = int(rating_value)
#             except ValueError:
#                 messages.error(request, "Invalid rating value. Please enter a valid number.")
#                 return redirect('turf')

#             # Check if the user already has a rating for the given turf
#             existing_rating = RatingDB.objects.filter(turf=turf, user=user).first()

#             if existing_rating:
#                 # If a rating already exists, update it
#                 existing_rating.Rating = rating
#                 existing_rating.save()
#                 messages.success(request, "Rating updated successfully.")
#             else:
#                 # If no existing rating, create a new one
#                 rating_instance = RatingDB(turf=turf, user=user, Rating=rating)
#                 rating_instance.save()
#                 messages.success(request, "Rating added successfully.")

#             # Calculate overall rating for the turf
#             ratings = RatingDB.objects.filter(turf=turf)
#             total_ratings = ratings.count()

#             if total_ratings == 0:
#                 overall_rating = 0  # No ratings yet
#             else:
#                 sum_ratings = sum(rating.Rating for rating in ratings if rating.Rating is not None)
#                 overall_rating = sum_ratings / total_ratings

#             # Update the overall_rating field in the Turf model
#             turf.overall_rating = overall_rating
#             turf.save()

#             return redirect('turf')

#         except Turf.DoesNotExist:
#             messages.error(request, "Invalid turf.")
#             return redirect('turf')

#     else:
#         messages.error(request, "Invalid request method.")
#         return render(request, 'rating.html')
from django.shortcuts import render, get_object_or_404
from .models import Turf, RatingDB

def saverating(request, turf_id):
    if request.method == "POST":
        rating_value = request.POST.get('property_rating')

        try:
            turf = get_object_or_404(Turf, id=turf_id)
            user = request.user

            try:
                rating = int(rating_value)
            except ValueError:
                messages.error(request, "Invalid rating value. Please enter a valid number.")
                return redirect('turf')

            existing_rating = RatingDB.objects.filter(turf=turf, user=user).first()

            if existing_rating:
                existing_rating.Rating = rating
                existing_rating.save()
                messages.success(request, "Rating updated successfully.")
            else:
                rating_instance = RatingDB(turf=turf, user=user, Rating=rating)
                rating_instance.save()
                messages.success(request, "Rating added successfully.")

            ratings = RatingDB.objects.filter(turf=turf)
            total_ratings = ratings.count()

            overall_rating = 0
            if total_ratings != 0:
                sum_ratings = sum(rating.Rating for rating in ratings if rating.Rating is not None)
                overall_rating = sum_ratings / total_ratings

            turf.overall_rating = overall_rating
            turf.save()

            return redirect('turf')

        except Turf.DoesNotExist:
            messages.error(request, "Invalid turf.")
            return redirect('turf')

    else:
        messages.error(request, "Invalid request method.")
        turf = get_object_or_404(Turf, id=turf_id)
        return render(request, 'rating.html', {'turf': turf})

def get_overall_rating(request):
    if request.method == 'GET':
        turf_id = request.GET.get('turfId')

        try:
            turf = Turf.objects.get(id=turf_id)
            ratings = RatingDB.objects.filter(turf=turf)
            total_ratings = ratings.count()

            if total_ratings == 0:
                overall_rating = 0  # No ratings yet
            else:
                sum_ratings = sum(rating.Rating for rating in ratings)
                overall_rating = sum_ratings / total_ratings

            # Check if the user has given a rating for this turf
            user = request.user
            if user.is_authenticated:
                user_rating = RatingDB.objects.filter(turf=turf, user=user).first()
                if user_rating:
                    # Update overall rating considering the latest user rating
                    sum_ratings += user_rating.Rating
                    total_ratings += 1
                    overall_rating = sum_ratings / total_ratings

            # Return both overall rating and user count
            return JsonResponse({'overallRating': overall_rating, 'userCount': total_ratings})

        except Turf.DoesNotExist:
            return JsonResponse({'error': 'Invalid turf ID'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def feedback(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback')

        if name:
            feedback = Feedback(name=name, email=email, feedback=feedback_text, turf=turf)
            feedback.save()
            return JsonResponse({"message": "Feedback submitted successfully."})
        else:
            return JsonResponse({"error": "Name cannot be empty."}, status=400)
    else:
        # Fetch all feedback entries for the current turf
        feedback_entries = Feedback.objects.filter(turf=turf)
        return render(request, 'feedback.html', {'turf_id': turf_id, 'feedback_entries': feedback_entries})

def feedback_notification(request,user_id):
    user = get_object_or_404(User, pk=user_id)  # Assuming you have a User model
    turfs = Turf.objects.filter(user=user)
    
    turf_feedbacks = {}  # Dictionary to store turf and its feedbacks

    for turf in turfs:
        feedbacks = Feedback.objects.filter(turf_id=turf)
        turf_feedbacks[turf] = feedbacks
    context = {'user': user, 'turf_feedbacks': turf_feedbacks}
    
    return render(request, 'feedback_notification.html', context)


# def turf(request):
#     # Get the TurfCategory queryset with prefetch_related()
#     turf_category_queryset = TurfCategory.objects.prefetch_related()

#     # Get the user and user's role
#     user = request.user
#     roll = get_user_role(user.id)  # Assuming you have a get_user_role function

#     if request.method == 'POST':
#         category_id = request.POST.get('categoryId')
#         keyword = request.POST.get('keyword')

#         try:
#             if category_id is not None and keyword is not None:
#                 # Filter Turf objects based on category_id and name__istartswith
#                 turfs = Turf.objects.filter(turfcategory=category_id, name__istartswith=keyword)
#             elif  category_id is not None:
#                 turfs = Turf.objects.filter(turfcategory=category_id)
#             elif keyword is not None:
#                 turfs = Turf.objects.filter(name__istartswith=keyword)  
#             if turfs.exists():
#                 # Create a list of dictionaries containing turf information
#                 turflist = [{'image': turf.img.url, 'name': turf.name, 'description': turf.description, 'turf_id': turf.id} for turf in turfs]

#                 return JsonResponse({'turflist': turflist})
#             else:
#                 # Handle the case where no turfs match the search criteria
#                 return JsonResponse({"message": "No matching turfs found."}, status=404)

#         except Turf.DoesNotExist:
#             # Handle other exceptions if necessary
#             return JsonResponse({"message": "An error occurred during the search."}, status=500)

#     else:
#         # If the request method is not POST, retrieve all Turf objects
#         turf_objects = Turf.objects.all()

#         # Prepare the context dictionary
#         dict_turf = {
#             'turf_category': turf_category_queryset,
#             'turf': turf_objects,
#             'roll': roll  # Add user's role to the context
#         }

#         # Render the turf.html template with the context
#         return render(request, "turf.html", dict_turf)


def turf(request):
    # Get the TurfCategory queryset with prefetch_related()
    turf_category_queryset = TurfCategory.objects.prefetch_related()

    # Get the user and user's role
    user = request.user
    roll = get_user_role(user.id)  # Assuming you have a get_user_role function

    if request.method == 'POST':
        category_id = request.POST.get('categoryId')
        keyword = request.POST.get('keyword')

        try:
            if category_id is not None and keyword is not None:
                # Filter Turf objects based on category_id and name__istartswith
                turfs = Turf.objects.filter(turfcategory=category_id, name__istartswith=keyword)
            elif  category_id is not None:
                turfs = Turf.objects.filter(turfcategory=category_id)
            elif keyword is not None:
                turfs = Turf.objects.filter(name__istartswith=keyword)  
            if turfs.exists():
                # Create a list of dictionaries containing turf information
                turflist = [{'image': turf.img.url, 'name': turf.name, 'description': turf.description, 'turf_id': turf.id} for turf in turfs]

                return JsonResponse({'turflist': turflist})
            else:
                # Handle the case where no turfs match the search criteria
                return JsonResponse({"message": "No matching turfs found."}, status=404)

        except Turf.DoesNotExist:
            # Handle other exceptions if necessary
            return JsonResponse({"message": "An error occurred during the search."}, status=500)

    else:
        # If the request method is not POST, retrieve all Turf objects
        turf_objects = Turf.objects.all()

        # Prepare the context dictionary
        dict_turf = {
            'turf_category': turf_category_queryset,
            'turf': turf_objects,
            'roll': roll  # Add user's role to the context
        }

        # Render the turf.html template with the context
        return render(request, "turf.html", dict_turf)





# def turflist_edit(request,turf_id):
#     user_id = request.session.get('session1')
#     locations =Location.objects.all()
#     category=TurfCategory.objects.all()
#     turf = Turf.objects.filter(user_id=user_id).first()
#     multi_image=Turf_multi_image.objects.all()
#     turf_edit={
#         'turf': turf,
#         'category': category,
#         'locations': locations,
#         'multi_image': multi_image

#     }
   
#     return render(request,'turflist_edit.html', turf_edit )
def turflist_edit(request, turf_id):
    user_id = request.user.id
    locations = Location.objects.all()
    category = TurfCategory.objects.all()
    
   
    turf = Turf.objects.get(user_id=user_id, id=turf_id)
   
    # Count bookings related to the Turf object
    booking_count = Booking.objects.filter(turf=turf).count()

    multi_images = Turf_multi_image.objects.filter(turf=turf)
    
    turf_edit = {
        'turf': turf,
        'category': category,
        'locations': locations,
        'multi_images': multi_images,
        'booking_count': booking_count,

    }

        # Print debug information
    print(f'Booking Count: {booking_count}')

    return render(request, 'turflist_edit.html', turf_edit)


   
  
# def turflist_edit_save(request):
#     user_id = request.session.get('session1')
#     if request.method == 'POST':
#             name = request.POST.get('name')
#             image=request.FILES.get('image')
#             address = request.POST.get('address')
#             description = request.POST.get('description')
#             multi_images=request.POST.getlist('newsfeedsmuloverall-ratingtipleimg[]') 
#             turfcategory_id = request.POST.get('category')
#             location_id = request.POST.get('location') 
#             amount=request.POST.get('amount')
#             advertisement_image=request.FILES.get('advertisement_image')

#             # ids = request.session.get('session1')
#             # profile = Profile.objects.get(user_id=ids)
#             # user = profile.user
#             # user.username = username
#             # user.email = email
#             turf = Turf(name=name,img=image, address=address, description=description,  turfcategory_id=turfcategory_id, location_id=location_id, amount=amount, advertisement_image=advertisement_image, user_id=user_id )
#             turf.save()


#             #  # Update profile data, including the image
#             # if image:
#             #     profile.image = image

#             # profile.name = name
#             # profile.address = address
#             # profile.place = place
#             # profile.country = country
#             # profile.district = district
#             # profile.save()
#             # return redirect('profile')
#     return render(request,'turflist_edit.html')
def turf_creation(request):
    user_id = request.user.id
    locations = Location.objects.all()
    category = TurfCategory.objects.all()
    multi_image = Turf_multi_image.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        description = request.POST.get('description')
        multi_images = request.POST.getlist('newsfeedsmultipleimg[]')
        turfcategory_id = request.POST.get('category')
        location_id = request.POST.get('location')
        amount = request.POST.get('amount')
        advertisement_image = request.FILES.get('addimage')

        # Check for required fields and handle errors
        if not all([name, image, address, description, turfcategory_id, location_id, amount]):
            return JsonResponse({'error': 'All fields are required'})

        # Create a Turf object with required fields
        turf = Turf(name=name, img=image, address=address, description=description, turfcategory_id=turfcategory_id,
                    location_id=location_id, amount=amount, user_id=user_id)
        turf.save()

        # Get the ID of the newly created Turf object
        turf_id = turf.id
        print(turf_id)
        print(multi_images)

        # Save advertisement image if provided
        if advertisement_image:
            turf.advertisement_image = advertisement_image
            turf.save()

        # Save multi_images
        for multimage in multi_images:
            # Create an instance of Turf_multi_image and associate it with the Turf
            turf_multi_image = Turf_multi_image(img=multimage, turf=turf)
            turf_multi_image.save()

        return JsonResponse({'message': 'Turf and Images uploaded successfully', 'id': turf_id})

    return render(request, 'turf-creation.html', {'locations': locations, 'category': category, 'user_id': user_id})
# def turf_creation(request):
#     user_id = request.user.id
#     locations =Location.objects.all()
#     category=TurfCategory.objects.all()
#     multi_image=Turf_multi_image.objects.all()
   
#     if request.method == 'POST':
#             name = request.POST.get('name')
#             image=request.FILES.get('image')
#             address = request.POST.get('address')
#             description = request.POST.get('description')
#             multi_images=request.POST.getlist('newsfeedsmultipleimg[]') 
#             turfcategory_id = request.POST.get('category')
#             location_id = request.POST.get('location') 
#             amount=request.POST.get('amount')
#             advertisement_image=request.FILES.get('addimage')


#             #  Check for required fields and handle errors
#             if not all([name, image, address, description, turfcategory_id, location_id, amount, advertisement_image]):
#                 return JsonResponse({'error': 'All fields are required'})


#             turf = Turf(name=name,img=image, address=address, description=description,  turfcategory_id=turfcategory_id, location_id=location_id, amount=amount, advertisement_image=advertisement_image, user_id=user_id )
#             turf.save()

#             # Get the ID of the newly created Turf object
#             turf_id = turf.id
#             print(turf_id)
#             print(multi_images)
            
#             for multimage in multi_images:
#                     # Create an instance of Turf_multi_image and associate it with the Turf
#                     turf_multi_image = Turf_multi_image(img=multimage, turf=turf)
#                     turf_multi_image.save()

#             return JsonResponse({'message': 'Turf and Images uploaded successfully', 'id': turf_id})


#     return render(request, 'turf-creation.html', {'locations': locations, 'category': category,'user_id':user_id}) 

def upload_image(request):
    if request.method == 'POST':
        form = MultipleImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('img')  # Fetch multiple images
            
            for image in images:
                uploaded_image = form.save(commit=False)
                uploaded_image.img = image  # Assign the image file
                uploaded_image.save() 
                # Save each image to the database
            
                return JsonResponse({
                    'success': True,
                    'url': uploaded_image.img.url,
                    'image_id': uploaded_image.id,
                    'name': uploaded_image.img.name
                })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def delete_uploaded_image(request):
      try:
        image_id = request.POST.get('image_id')
        print('image_id',image_id)
        # Check if the object exists
        image = Turf_multi_image.objects.filter(id=image_id).first()
        print('image',image)
        print(image)
        if image:
            image.delete()  # Delete the image from the database
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': 'Image does not exist or has already been deleted'})

      except Exception as e:
        return JsonResponse({'success': False, 'error_message': str(e)})
    

def editimg_delete_image(request):
    try:
        image_id = request.POST.get('image_id')
        
        # Check if the object exists
        image = Turf_multi_image.objects.filter(id=image_id).first()
        if image:
            image.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': 'Image does not exist or has already been deleted'})

    except Exception as e:
        return JsonResponse({'success': False, 'error_message': str(e)}) 


# def turflist_edit_save(request):
#     if request.method == 'POST':
#         turf_id = request.POST.get('turfid')
#         print(turf_id)
#         turf_get=get_object_or_404(Turf, id=turf_id)
#         print(turf_id)

#         if turf_get:
#             turf_get.name = request.POST.get('name')
#             turf_get.address = request.POST.get('address')
#             turf_get.description = request.POST.get('description')
#             turf_get.turfcategory_id = request.POST.get('category')
#             turf_get.location_id = request.POST.get('location')
#             turf_get.amount = request.POST.get('amount')
#             turf_get.img = request.FILES.get('image')
#             turf_get.advertisement_image = request.FILES.get('advertisement_image')
#             turf_get.save()
#             turf_get.id

#             # Handling multiple images
#             images = request.FILES.getlist('newsfeedsmultipleimg[]')
#             for img in images:
#                 new_image = Turf_multi_image(img=img, turf=turf_id)
#                 new_image.save()
#             return JsonResponse({"message": "Updated successfully"})

#     return JsonResponse({"message": "Failed to update"})


# def editupload_image(request):
#     if request.method == 'POST':
#         form = MultipleImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             images = request.FILES.getlist('img')  # Fetch multiple images
            
#             for image in images:
#                 uploaded_image = form.save(commit=False)
#                 uploaded_image.img = image  # Assign the image file
#                 uploaded_image.save() 
#                 # Save each image to the database
            
#                 return JsonResponse({
#                     'success': True,
#                     'url': uploaded_image.img.url,
#                     'image_id': uploaded_image.id,
#                     'name': uploaded_image.img.name
#                 })
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors})
#     return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def turflist_edit_save(request):  
    if request.method == 'POST':
        turfcategory_id = request.POST.get('category')
        name = request.POST.get('name')
        amount = request.POST.get('price')
        location_id=request.POST.get('location')
        address=request.POST.get('address')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        img = request.FILES.get('turf_image')
        multi_images = request.FILES.getlist('newsfeedsmultipleimg[]')
        advertisement_image = request.FILES.get('advertisement_image')
        turf_id=request.POST.get('turfid')

        # Check if the Product instance exists
        turf_value = get_object_or_404(Turf, id=turf_id)

        turf_value.turfcategory_id = turfcategory_id
        turf_value.name = name
        turf_value.address=address
        turf_value.amount = amount
        turf_value.description = description
        turf_value.location_id = location_id
        
        if 'turf_image' in request.FILES:
            turf_value.img = request.FILES['turf_image']
            print(turf_value.img)

        
        if 'advertisement_image' in request.FILES:
            turf_value.advertisement_image = request.FILES['advertisement_image']
            
        turf_value.save()
        trd_id=turf_value.id

        for multimage in multi_images:
            new_multi_img = Turf_multi_image(img=multimage, turf_id=trd_id) 
            new_multi_img.save()

        multi_img = Turf_multi_image.objects.filter(turf_id=turf_id)
        return redirect('myprofile')

        
def editupload_image(request):
    if request.method == 'POST':
        turf_id = request.POST.get('turfid')
        images = request.FILES.getlist('newsfeedsmultipleimg[]')

        for img in images:
            new_image = Turf_multi_image(image=img, turf_id=turf_id)
            new_image.save()

        return JsonResponse({'success': True, 'message': 'Images uploaded successfully'})

    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def contact(request):
    contact_details = Contact.objects.all()
    return render(request, 'contact.html', {'contact_details': contact_details}) 


def display_category(request, category_id):
    user = request.user
    roll = get_user_role(user.id)  # Assuming you have a get_user_role function
    # Retrieve the TurfCategory instance
    turf_category = TurfCategory.objects.all()

    category = get_object_or_404(TurfCategory, id=category_id)

    # Query Turfs related to the category using the appropriate field name
    turfs_in_category = Turf.objects.filter(turfcategory=category)

    return render(request, 'category.html', {'category': category, 'turfs_in_category': turfs_in_category,'turf_category':turf_category,'roll':roll},)
   



    