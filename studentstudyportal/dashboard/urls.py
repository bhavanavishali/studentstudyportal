from . import views
from django.urls import path
app_name = 'dashboard'

urlpatterns = [
    path('',views.home,name='home'),
    path('notes/',views.notes,name='notes'),
    path('delete_note/<int:pk>/',views.delete_note,name='delete_note'),
    path('notes_detail/<int:pk>/',views.NotesDetailView.as_view(),name='notes_detail'),
    
]