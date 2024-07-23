from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from hr.models import JobPost , CandidateApplications , SelectCandidateJob
from candidate.models import IsSortList
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json;
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

@login_required
def hrHome(request):
    jobposts = JobPost.objects.filter(user=request.user)

    print(jobposts)
    return render(request,'hr/hrdashbordh.html',{'jobposts':jobposts})

@login_required
def hrDashboard(request):
    # jobpost = JobPost.objects.all()
    return render(request,'hr/chat/dashboard.html')

@login_required
def hrCandidateDetails(request,id):
    if JobPost.objects.filter(id=id).exists():
        jobpost = JobPost.objects.get(id=id)
        jobapplys = CandidateApplications.objects.filter(job=jobpost)
        print('=============')
        print(jobapplys)
        selectedCandidate = SelectCandidateJob.objects.filter(job=jobpost)
        print(selectedCandidate)
        return render(request,'hr/candidate.html',{'jobapplys':jobapplys,'jobpost':jobpost,'selectedCandidate':selectedCandidate})
    else:
        return render('hrdash') 

@login_required
def postJobs(request):
    if request.method == 'POST':
        job_title = request.POST.get('job-title')
        address = request.POST.get('address')
        company_name = request.POST.get('company-name')
        salary_low = request.POST.get('salary-low')
        salary_high = request.POST.get('salary-high')
        last_date  = request.POST.get('last-date')

        jobpost = JobPost(user=request.user,title=job_title,address=address,compnayName=company_name,salaryLow=salary_low,salaryHigh=salary_high,lastDateToApply=last_date)
        jobpost.save()
        msg = "Job Upload Done.."
        return render(request,'hr/postjob.html',{'msg':msg})
    return render(request,'hr/postjob.html')

def acceptApplication(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid') 
        candidate = CandidateApplications.objects.get(id=candidateid) 
        jobpost = JobPost.objects.get(id=jobpostid)
        if SelectCandidateJob.objects.filter(candidate=candidate).exists()==False:
            SelectCandidateJob(job=jobpost,candidate=candidate).save()
            IsSortList(user=candidate.user,job=jobpost).save()
        return redirect('/candidatedetails/'+str(jobpostid)+"/")
    return redirect('hrdash')


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
                bot_response = "Sure, test I can help you find job listings. What type of job are you interested in?"
            elif 'my profile' in message:
                current_step = 'my_profile'
                user = request.user
                print('0000000000')
                print(user)
                bot_response = "here are your profile details:"
            elif 'hi' in message:
                bot_response = "hi",
            elif 'hello' in message:
                bot_response = "hello sir!",
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