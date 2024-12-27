from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
# from .views import *
# from . import views - > views.viewname.as_view()
from . import views 

 

urlpatterns = [

    path('login/',views.BaseLogin.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/',views.BaseRegister.as_view(),name='register'),
    
    path('',views.BaseHome.as_view(),name='home'),
    path('home/',views.BaseHome.as_view(),name='home'),
    path('search/',views.search, name='search'),
 
    path('profile/',views.BaseProfile.as_view(), name='profile'), 
    path('profile_edit/',views.BaseProfileEdit.as_view(), name='profile_edit'), 
    path('remove-all-anime/', views.RemoveAllAnime.as_view(), name='remove_all_anime'),
    path('add-anime/', views.AddAnime.as_view(), name='add_anime'),

 
    path('anime/<str:title>/',views.BaseAnimeDetail.as_view(),name='anime-detail'), 
    path('watch/<str:title>/<str:episode_no>/', views.BaseAnimeWatch.as_view(), name='watch'),
   
 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


