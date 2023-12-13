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