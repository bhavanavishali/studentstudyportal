from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Notes
from .forms import *
from django.views import generic
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