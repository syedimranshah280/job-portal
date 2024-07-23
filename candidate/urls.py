from django.urls import path
from candidate import views
urlpatterns = [
     path('profile/',views.candidateHome,name='profile'),
     path('dash/',views.candidateDashboard,name='dashboard'),
     path('applyjob/<int:id>/',views.applyJob,name='apply'),
     path('applylist/',views.myjoblist,name='mylist'),
     path('chatbot/', views.chatbot, name='chatbot'),
     path('get_response/', views.chatbot_response, name='chatbot_response'),
]
