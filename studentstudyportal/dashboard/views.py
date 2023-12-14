from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Notes
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests



# Create your views here.
def home(request):
    return render(request,'home.html')

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

def delete_note(request,pk=None):
    note = Notes.objects.get(id=pk)
    note.delete()
    print('deleted')
    return redirect('dashboard:notes')

class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'notes_detail.html'
    context_object_name = 'notes'


#..............................Homework................................................


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

def youtube(request):
    if request.method =='POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=20)
        result_list =[]
        for i in video.result()['result']:
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
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']= desc
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

def book(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = request.POST['text']
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text
            try:
                r = requests.get(url)
                r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
                answer = r.json()
                result_list = []
                for i in range(min(10, len(answer.get('items', [])))):
                    volume_info = answer['items'][i].get('volumeInfo', {})
                    
                    result_dict = {
                        'title': volume_info.get('title', 'N/A'),
                        'subtitle': volume_info.get('subtitle', ''),
                        'description': volume_info.get('description', ''),
                        'count': volume_info.get('pageCount', 0),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('pageRating', 0.0),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'preview': volume_info.get('previewLink', ''),
                    }

                    result_list.append(result_dict)

                context = {'form': form, 'results': result_list}
                return render(request, 'books.html', context)

            except requests.RequestException as e:
                # Handle exceptions related to the request (e.g., network error, bad response)
                error_message = f"Error during request: {str(e)}"
                context = {'form': form, 'error_message': error_message}
                return render(request, 'books.html', context)

    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'books.html', context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = request.POST['text']
            url = "https://api.dictionary.api.dev/api/v2/entries/en_US/"+text
            r = requests.get(url)
            answer = r.json()
            try:
                # Extracting information from the API response
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                example = answer[0]['meanings'][0]['definitions'][0]['example']
                synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

                # Creating a context dictionary with extracted information
                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms
                }

            except:
                # Handling the case when the API response structure is not as expected
                context = {
                    'form': form,
                    'input': text
                }

        # Render the 'dictionary.html' template with the context
        return render(request, 'dictionary.html', context)

    else:
        # Handling the GET request (initial page load)
        form = DashboardForm()
        context = {'form': form}

    # Render the 'dictionary.html' template with the context
    return render(request, 'dictionary.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!!")
            #redirect ('dashboard:login')
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'register.html',context)
