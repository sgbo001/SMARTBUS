
from django.urls import path
from reviews.views import ReviewCreateView

app_name = 'reviews' 

urlpatterns = [
    path('create/', ReviewCreateView.as_view(), name='review_create'),


]