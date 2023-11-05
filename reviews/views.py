from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from .models import Review
from bus.models import Bus  # Adjust this import based on your app structure
from .forms import ReviewForm
from django.contrib.auth.models import User
from bus.models import BusStop, Bus, BusRoute
from django.contrib import messages
import json
import pandas as pd

def search_buses_by_stop(request):
    if request.method == 'GET':
        stop_name = request.GET.get('stop_name', '')
        buses = Bus.objects.filter(stop_points__stop_point__icontains=stop_name)
        return render(request, 'search_form.html', {'buses': buses})
    
    
class ReviewCreateView(View):
    template_name = 'search_form.html'

    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        stop_name = request.GET.get('stop_name', '')
        bus_id = request.GET.get('bus_id', '')
        
        is_number = stop_name and stop_name[0].isdigit()


        if is_number:
            bus_info = BusRoute.objects.filter(stop_point=stop_name)
            unique_stop_names = bus_info.values('common_name').distinct()
            unique_bus_ids = bus_info.values('bus_id').distinct()
            #unique_arrival_times = bus_info.values('arrival_time').distinct()
     
        else:
            bus_info = BusRoute.objects.filter(common_name=stop_name)
            unique_stop_names = bus_info.values('stop_point').distinct()
            unique_bus_ids = bus_info.values('bus_id').distinct()
            #unique_arrival_times = bus_info.values('arrival_time').distinct()

        unique_arrival_times = bus_info.values('arrival_time').distinct() 
        for arrival_time in unique_arrival_times:
            print(arrival_time['arrival_time'])


        return render(request, self.template_name, {'form': form, 'unique_bus_ids': unique_bus_ids, 'unique_common_names': unique_stop_names, 'unique_arrival_times': unique_arrival_times,})
    
   
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            #stop_name = request.GET.get('stop_name')
            bus_id = request.POST.get('bus_id')
            arrival_time = request.POST.get('arrival_time')
            stop_name = request.GET.get('stop_name')
            if request.user.is_authenticated:
                first_name = request.user.first_name
                last_name = request.user.last_name
                full_name = f"{first_name} {last_name}"
            else:
                full_name = "Guest" 
            
            if stop_name.isdigit():
                stop_point = stop_name

            else:
                stop_point = BusRoute.objects.filter(common_name=stop_name).values('stop_point').distinct()

                
            review = form.save(commit=False)
            review.stop_point = stop_point
            review.bus_id = bus_id
            review.arrival_time = arrival_time
            review.full_name = full_name
            review.save()
            messages.success(request, 'Review submitted successfully.')
            previous_page = '/home'
            return redirect(previous_page)
        else:
            messages.warning(request, 'An error occurred while saving this review.')


