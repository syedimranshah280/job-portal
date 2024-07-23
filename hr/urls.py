from django.urls import path
from hr import views
urlpatterns = [
    path('hrprofile/',views.hrHome,name='hrprofile'),
    path('hrdash/',views.hrDashboard,name='hrdash'),
    path('candidatedetails/<int:id>/',views.hrCandidateDetails,name='candidatedetails'),
    path('postjob/',views.postJobs,name='postjob'),
    path('acceptapplication/',views.acceptApplication,name='acceptapplication'),

    # path('chatbot/', views.chatbot, name='chatbot'),

    path('employer/get_response/', views.chatbot_response, name='chatbot_response'),
     
]
