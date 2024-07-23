from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from hr.models import JobPost , CandidateApplications
from candidate.models import MyApplyJobList
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json;
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# Create your views here.

@login_required
def candidateHome(request):
    jobpost = JobPost.objects.all()
    return render(request,'candidate/dashboradh.html',{'jobpost':jobpost})
def candidateDashboard(request):
    # jobpost = JobPost.objects.all()
    return render(request,'candidate/chat/dashboard.html')

@login_required
def applyJob(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        college = request.POST.get('college')
        passing_year = request.POST.get('passing_year')
        yearOfExperience = request.POST.get('yearOfExperience')
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
        else:
            resume = None
        print(resume)
        print('=========')
        job = JobPost.objects.get(id=id)
        if CandidateApplications.objects.filter(user=request.user,job=job).exists():
            return redirect('dashboard')
        CandidateApplications(user=request.user,job=job,passingYear=passing_year,yearOfExperience=yearOfExperience,resume=resume).save()
        return redirect('dashboard')
    return render(request,'candidate/apply.html')

@login_required
def myjoblist(request):
    joblist = MyApplyJobList.objects.filter(user=request.user)
    print(joblist)
    return render(request,'candidate/myjoblist.html',{'joblist':joblist})

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = request.POST.get('message')
        response = get_response(data)
        return JsonResponse({'response': response})
    return render(request, 'chatbot/chat.html')

def get_response(message):
    # Your chatbot logic goes here
    # if 'help' in message.lower():
    #     return "Sure! How can I assist you today?"
    # elif 'profile' in message.lower():
    #     return "Are you looking to update your profile information?"
    # elif 'jobs' in message.lower():
    #     return "I can help you find job listings. What type of job are you interested in?"
    # else:
    #     return "I'm sorry, I didn't understand that. Can you please rephrase?"

    with open('qa_data.json', 'r') as file:
        qa_data = json.load(file)
    questions = qa_data['questions']
    for qa in questions:
        if message.lower() == qa['question'].lower():
            return qa['answer']
    return "I'm sorry h, I didn't understand that. Can you please rephrase?"


def chatbot_response(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            chatbot = JobChatbot()
            response = chatbot.get_response(request,message)
            return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)


class JobChatbot:
    def __init__(self):
        nltk.download('wordnet')    
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
        tokens = [token for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)

    def get_response(self,request, message):
        last_question = '<p>Hi there 👋<br>How can I help you today? <br>Please type any option from the following to proceed:<br>1. My Profile<br>2. Find job<br>3. Job status</p>'
        processed_message = self.preprocess_text(message)
        print('=======LS=================')
        print(request.session.get('last_question'))
        print('========================')
        # print('pre',processed_message )
        
        # Simple response generation logic
        bot_response = ''
        current_step = 'home'
        if current_step == 'home':
            if 'job' in message:
                bot_response = "Sure, I can help you find job listings. What type of job are you interested in?"
            elif 'my profile' in message:
                current_step = 'my_profile'
                user = request.user
                print('0000000000')
                print(user)
                bot_response = "here are your profile details:"
            elif 'profile' in message:
                bot_response = "Yes, you can update your profile information by logging into your account and navigating to the profile section."
            elif 'company' in message:
                bot_response = "Our company's mission is to provide innovative solutions to our customers' problems."
            else:
                bot_response = "I'm sorry, I didn't understand that. Can you please rephrase?"
        elif current_step == 'my_profile':
            if 'job' in message:
                bot_response = "Sure, I can help you find job listings. What type of job are you interested in?"
            elif 'my profile' in message:
                bot_response = "here are your profile details:"
            elif 'profile' in message:
                bot_response = "Yes, you can update your profile information by logging into your account and navigating to the profile section."
            elif 'company' in message:
                bot_response = "Our company's mission is to provide innovative solutions to our customers' problems."
            else:
                bot_response = "I'm sorry, I didn't understand that. Can you please rephrase?"
        request.session['last_question'] = bot_response
        request.session['current_step'] = current_step
        
        return bot_response