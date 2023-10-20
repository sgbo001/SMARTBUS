from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from .models import Review
from bus.models import Bus  # Adjust this import based on your app structure
from .forms import ReviewForm
from django.contrib.auth.models import User
from bus.models import BusStop, Bus
from django.contrib import messages

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
        is_number = stop_name and stop_name[0].isdigit()

        if is_number:
            buses = Bus.objects.filter(stop_points__stop_point__icontains=stop_name)
            stop_points = list(set(stop_point.common_name for bus in buses for stop_point in bus.stop_points.all()))
        else:
            buses = Bus.objects.filter(stop_points__common_name__icontains=stop_name)
            stop_points = list(set(stop_point.stop_point for bus in buses for stop_point in bus.stop_points.all()))

        return render(request, self.template_name, {'form': form, 'buses': buses, 'stop_points': stop_points})

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            stop_name = request.GET.get('stop_name')
            bus_id = request.POST.get('bus_id')
            
            is_number = stop_name and stop_name[0].isdigit()
            
            try:
                if is_number:
                    stop_point = BusStop.objects.get(stop_point=int(stop_name))
                else:
                    stop_point = BusStop.objects.get(common_name=stop_name)
                
                bus = Bus.objects.get(bus_id=bus_id)
            except BusStop.DoesNotExist:
                # Handle the case where the stop_name doesn't exist
                return JsonResponse({'errors': 'Invalid stop name'}, status=400)
            except Bus.DoesNotExist:
                # Handle the case where the bus_id doesn't exist
                return JsonResponse({'errors': 'Invalid bus ID'}, status=400)
            
            review = form.save(commit=False)
            review.stop_point = stop_point
            review.bus_id = bus
            review.save()
            messages.success(request, 'Review submitted successfully.')
            previous_page = '/home'
            return redirect(previous_page)
        else:
            messages.warning(request, 'An error occurred while saving this review.')

    