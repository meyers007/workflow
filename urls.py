from django.urls import path
from . import views

app_name = 'workflow'

urlpatterns = [
    path('LINK/',  views.index , name='wf urls1'),
]
