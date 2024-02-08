from . import views
from django.urls import path
app_name = 'dashboard'

urlpatterns = [
    path('',views.home,name='home'),
    path('notes/',views.notes,name='notes'),
    path('delete_note/<int:pk>/',views.delete_note,name='delete_note'),
    path('notes_detail/<int:pk>/',views.NotesDetailView.as_view(),name='notes_detail'),
    path('pdf/<int:pk>/',views.generatePDF,name='pdf'),
    

    #..................Homework....................................

    path('homework/',views.homework,name='homework'),
    path('update_homework/<int:pk>/',views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>/',views.delete_homework,name='delete_homework'),

    path('youtube/',views.youtube,name='youtube'),

    path('dictionary/',views.dictionary,name='dictionary'),

    path('book/',views.book,name='book'),

    path('logout/',views.logout,name='logout'),
    
]