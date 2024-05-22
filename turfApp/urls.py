from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('turf/' , views.turf, name='turf'),
    # path('contact/' , views.contact, name='contact'),
    path('user_register/' , views.user_register, name='user_register'),
    path('login_page/' , views.login_page, name='login_page'),
    path('success_login/' , views.success_login, name='success_login'),
    path('turf_creation/' , views.turf_creation, name='turf_creation'),
    #path('turf_singlepage/' , views.turf_singlepage, name='turf_singlepage')
    path('turf-singlepage/<int:turf_id>/', views.turf_singlepage, name='turf_singlepage'),
    path('turf_booking/<int:turf_id>/' , views.turf_booking, name='turf_booking'),
    path('turf_booking_save/' , views.turf_booking_save, name='turf_booking_save'),
    path('upload_image/' , views.upload_image, name='upload_image'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('edit/',views.edit,name='edit'),
    path('edit_save/',views.edit_save,name='edit_save'),
    path('change_password/',views.change_password,name='change_password'),
    path('success_changepassword/',views.success_changepassword,name='success_changepassword'),
    path('turf_list/',views.turf_list,name='turf_list'),
    path('view_bookings/<int:turf_id>/',views.view_bookings,name='view_bookings'),
    path('turflist_edit/<int:turf_id>/',views.turflist_edit,name='turflist_edit'), 
    path('turflist_edit_save/',views.turflist_edit_save,name='turflist_edit_save'),
    path('delete_turf/',views.delete_turf,name='delete_turf'),
    path('notification/',views.notification,name='notification'),
    path('user_notification/',views.user_notification,name='user_notification'),
    path('cancel_booking/' , views.cancel_booking, name='cancel_booking'),
    path('logout/',views.logout_view, name='logout'),
    path('search_turf/',views.search_turf, name='search_turf'),
    path('feedback/<int:turf_id>/', views.feedback, name='feedback'),
    path('feedback_notification/<int:user_id>/', views.feedback_notification, name='feedback_notification'),
    path('delete_uploaded_image/',views.delete_uploaded_image,name='delete_uploaded_image/'),
    path('editimg_delete_image/',views.editimg_delete_image,name='editimg_delete_image'),
    path('upload_image/',views.upload_image,name='upload_image'),
    path('editupload_image/',views.editupload_image,name='editupload_image'),
    path('contact/',views.contact,name='contact'),
    path('category/<int:category_id>/', views.display_category, name='display_category'),
        path('saverating/<int:turf_id>/', views.saverating, name='saverating'),
        # path('rate/<int:turf_id>/',views.rate_turf, name='rate_turf'),
        path('get_overall_rating/', views.get_overall_rating, name='get_overall_rating'),
        
        

]
