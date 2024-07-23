from django.urls import path
from authuser import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('',views.home,name='home'),
     path('login/',views.login_user,name='login'),
     path('candidte-register/',views.candidateregister,name='register'),
     path('register/',views.register,name='register-user'),
     path('hr-register/',views.hrregister,name='register-hr'),
     path('logout/',views.logoutUser,name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)