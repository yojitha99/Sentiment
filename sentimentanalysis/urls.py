"""sentimovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from movieapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movieadd',views.movieadd),
    path('showmovie',views.showmovie),
    path('editmovie/<int:id>',views.editmovie),
    path('updatemovie/<int:id>',views.updatemovie),
    path('delmovie/<int:id>',views.delmovie),
    path('reviewadd/<int:id>',views.reviewadd),
    #path('storereview/<int:id>',views.storereview),
    path('showreview/<int:id>',views.showreview),
    path('editreview/<int:id>',views.editreview),
    path('showgraph/<int:id>',views.showgraph),
    path('updatereview/<int:id>',views.updatereview),
    path('delreview/<int:id>/<int:movieid>',views.delreview),
]
