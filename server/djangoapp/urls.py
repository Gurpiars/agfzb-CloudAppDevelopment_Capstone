from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [

    path('base/', views.base, name='base'),

    path('contact/', views.contact , name='contact'),

    path('about/', views.about, name='about'),

    path('registration/', views.registration, name='registration'),
    
    path('login/', views.login_req, name='login'),

    path('logout/', views.signout, name='logout'),

    path('singup/', views.signup, name='signup'),
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer_details/<int:dealerid>/', view=views.get_dealer_details, name='dealer_details'),
    # path for add a review view


    path(route='add_review/<int:dealerid>/', view= views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)