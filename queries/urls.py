from django.urls import path
from . import views

urlpatterns = [
    path('query1/', views.query1, name='query1'),
    path('query2/', views.query2, name='query2'),
    path('query3/', views.query3, name='query3'),
    path('query4/', views.query4, name='query4'),
    path('query5/', views.query5, name='query5'),
    path('query6/', views.query6, name='query6'),
    path('query7/', views.query7, name='query7'),
    path('query8/', views.query8, name='query8'),
    path('query9/', views.query9, name='query9'),
    path('query10/', views.query10, name='query10'),
    path('query11/', views.query11, name='query11'),
    path('query12/', views.query12, name='query12'),
    path('query13/', views.query13, name='query13'),
    path('query14/', views.query14, name='query14'),
]
