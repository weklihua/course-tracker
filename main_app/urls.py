from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses_index, name='index'),
    path('courses/<int:course_id>/', views.courses_detail, name='detail'),
    path('courses/create/', views.CourseCreate.as_view(), name='courses_create'),
    path('courses/<int:pk>/update/', views.CourseUpdate.as_view(), name='courses_update'),
    path('courses/<int:pk>/delete/', views.CourseDelete.as_view(), name='courses_delete'),
]
