from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from .models import Notes
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'home.html')
@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            
        messages.success(request,f"Notes added from {request.user.username} successfully!")
    else:
        form = NotesForm
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'notes.html',context)
@login_required
def delete_note(request,pk=None):
    note = Notes.objects.get(id=pk)
    note.delete()
    print('deleted')
    return redirect('dashboard:notes')

class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'notes_detail.html'
    context_object_name = 'notes'

#.......................................Download the note in PDF formate.....................

import pdfkit
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def generatePDF(request,pk):
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('dashboard:notes_detail',args=[pk])), False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file_name.pdf"'
    return response


#..............................Homework................................................

@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],due=request.POST['due'],is_finished= finished)
            homework.save()
        
        messages.success(request,f"Homework added from {request.user.username} successfully!")
    else:
        form = HomeworkForm
    homework = Homework.objects.filter(user=request.user)
    context = {'homeworks':homework,'form':form}
    return render(request,'homework.html',context)
@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('dashboard:homework')

def delete_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    homework.delete()
    print('deleted')
    return redirect('dashboard:homework')
#...............................................Youtube Search .................................
@login_required
def youtube(request):
    if request.method =='POST':
        form = DashboardForm(request.POST)    # Create a DashboardForm instance with the POST data
        text = request.POST['text']           # Retrieve the 'text' field from the POST data
        video = VideosSearch(text,limit=20)   # Use the VideosSearch class to search for videos on YouTube based on the provided text
        result_list =[]
        for i in video.result()['result']:      # Iterate through the search results and create a dictionary for each video
            result_dict ={
                'input':['text'],
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
                                                            
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']: #descriptionSnippet is to offer a brief preview or summary of the video's description, allowing users or developers to get an idea of the content without having to retrieve the full description
                    desc += j['text']
            result_dict['description']= desc    # Add the description to the result dictionary
            result_list.append(result_dict)
            context = {'form':form,'results':result_list}
            return render(request,'youtube.html',context)
    else:    
        form = DashboardForm()
    context = {'form':form}
    return render(request,'youtube.html',context)

#......................... Dictionary ............................

# def dictionary(request):
#     if request.method == 'POST':
#         form = DashboardForm(request.POST)
#         if form.is_valid():
#             text = request.POST['text']
#             url = "https://api.dictionary.api.dev/api/v2/entries/en_US/" + text
#             r = requests.get(url)
#             answer = r.json()
#             try:
#                 phonetics = answer[0]['phonetics'][0]['text']
#                 audio = answer[0]['phonetics'][0]['audio']
#                 definition = answer[0]['meanings'][0]['definitions'][0]['definition']
#                 example = answer[0]['meanings'][0]['definitions'][0]['example']
#                 synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
#                 contex ={
#                     'form':form,
#                     'input':text,
#                     'phonetics':phonetics,
#                     'audio':audio,
#                     'definition':definition,
#                     'example':example,
#                     'synonyms':synonyms
#                 }
#             except:
#                 context = {
#                     'form':form,
#                     'input':''
#                 }
#         return render(request,'dictionary.html',context)



#     else:
#         form = DashboardForm()
#     context = {'form':form}
#     return render(request,'dictionary.html',context)


# ......................................Book Search ............................
@login_required
def book(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = request.POST['text'] # Construct the URL for the Google Books API search
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text  
            try:
                r = requests.get(url)       # Make a GET request to the Google Books API
                r.raise_for_status()         # Raise an HTTPError for bad responses 
                answer = r.json()           # Parse the JSON response
                result_list = []
                for i in range(min(10, len(answer.get('items', [])))):       # Iterate through the first 10 items in the 'items' array of the response
                    volume_info = answer['items'][i].get('volumeInfo', {})       # Extract relevant information from the 'volumeInfo' field
                    
                    result_dict = {
                        'title': volume_info.get('title', 'N/A'),               # Create a dictionary with book information
                        'subtitle': volume_info.get('subtitle', ''),
                        'description': volume_info.get('description', ''),
                        'count': volume_info.get('pageCount', 0),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('pageRating', 0.0),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'preview': volume_info.get('previewLink', ''),
                    }

                    result_list.append(result_dict)                 # Append the result dictionary to the result_list

                context = {'form': form, 'results': result_list}    # Prepare a context dictionary with the form and search results
                return render(request, 'books.html', context)

            except requests.RequestException as e:
                # Handle exceptions related to the request (e.g., network error, bad response)
                error_message = f"Error during request: {str(e)}"
                context = {'form': form, 'error_message': error_message}
                return render(request, 'books.html', context)

    else:
        form = DashboardForm()    # If the request method is not POST, create an instance of DashboardForm   

    context = {'form': form}
    return render(request, 'books.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!!")
            return redirect ('login')
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'register.html',context)

def logout(request):
    auth.logout(request)
    return redirect('dashboard:home')


import openai   # Imports the OpenAI Python library, which allows interaction with the OpenAI API.
import os       # used here to access environment variable(Environment variables in Python are a way to store configuration settings, system paths, and other information outside of your Python code.)
from dotenv import load_dotenv  #It's used to load environment variables from a .env file
from django.shortcuts import render  

load_dotenv()       #function to load environment variables from a .env file

api_key = os.getenv("OPENAI_KEY", None)     #Retrieves the OpenAI API key from the environment variables

@login_required         #This decorator ensures that only authenticated users can access 
def dictionary(request):
    chatbot_response = None
    
    if api_key is not None and request.method == 'POST':
        
        openai.api_key = api_key
        user_input = request.POST.get('text')       #Retrieves the user's input from the POST data.
        prompt = user_input
        messages = [
                  
           {"role": "user", "content": user_input},     #Contains the content or text of the user's input
        ]
        response = openai.ChatCompletion.create(        #Sends a request to the OpenAI Chat API to generate a chatbot response based on the provided messages.
            model = "gpt-3.5-turbo",
            
            messages=messages,
            max_tokens=1000,
            stop="."
        )
        print(response)
        chatbot_response = response['choices'][0]['message']['content']  # Assign the response to chatbot_response
        print(chatbot_response)
    
    return render(request, 'dictionary.html', {'response':chatbot_response})  # Pass chatbot_response to the template


