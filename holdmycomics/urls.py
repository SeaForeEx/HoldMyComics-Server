"""
URL configuration for holdmycomics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from holdmycomicsapi.views import register_user, check_user, BookView, CustomerView, UserView, SearchView

# url.py sets up which url to use for viewing the data

router = routers.DefaultRouter(trailing_slash=False)
# trailing_slash=False tells the router to accept /gametypes instead of /gametypes/
router.register(r'books', BookView, 'book')
# the first parameter, r'books, sets up the url
# the second parameter, BookView, tells the server which view to use when it sees that url
# the third parameter, book, is called the base name. You’ll only see the base name if you get an error in the server
router.register(r'customers', CustomerView, 'customer')
router.register(r'users', UserView, 'user')
router.register(r'search', SearchView, 'search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user), 
]
