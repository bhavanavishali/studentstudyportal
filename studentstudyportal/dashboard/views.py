from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Notes
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch



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