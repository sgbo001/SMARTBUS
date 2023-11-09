from django.shortcuts import render, redirect
from .forms import SearchForm
import requests
from django.http import HttpResponse
from datetime import datetime
from .models import Bus, BusRoute
from reviews.models import Review
from django.db.models import Avg, Max
from reviews.models import Review
import math
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
# Create your views here.

load_dotenv()

TRANSPORT_API_KEY = os.getenv('TRANSPORT_API_KEY', 'default_api_key')
TRANSPORT_APP_ID = os.getenv('TRANSPORT_APP_ID', 'default_app_id')
COORDINATE_API_KEY = os.getenv('COORDINATE_API_KEY', 'default_coordinate_api_key')

# Use COORDINATE_API_KEY wherever needed in your code

    
def home(request):
   if request.user.is_authenticated:
        # User is signed in, redirect to 'route_plan'
        return redirect('route_plan')
   else:
        return render(request, 'home.html')
    
def error(request):

     return render(request, 'error.html')

def route_plan(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            # Process the form data and perform the search logic
            from_post_code = form.cleaned_data['from_post_code']
            to_post_code = form.cleaned_data['to_post_code']
            date_time = form.cleaned_data['date_time']
            # Perform search logic and return results
    else:
        form = SearchForm()
    return render(request, 'route_plan.html', {'form': form})


def display_route(request):
    # Fetch data from the API
    from_post_code = request.GET.get('from_post_code')
    to_post_code = request.GET.get('to_post_code')
    
    from_post_code_info = get_coordinates(from_post_code)
    to_post_code_info = get_coordinates(to_post_code)
    
    if from_post_code_info and to_post_code_info:
        from_longitude = from_post_code_info['lng']
        from_latitude = from_post_code_info['lat']

        to_longitude = to_post_code_info['lng']
        to_latitude = to_post_code_info['lat']

        # Your code to call the API and display the results can go here
        # ...
        date_time_str = request.GET.get('date_time')
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
        date = date_time_obj.strftime('%Y-%m-%d')
        time = date_time_obj.strftime('%H:%M')

        api_url = f'https://transportapi.com/v3/uk/public_journey.json?from=lonlat%3A{from_longitude}%2C{from_latitude}&to=lonlat%3A{to_longitude}%2C{to_latitude}&date={date}&time={time}&journey_time_type=leave_after&service=silverrail&modes=bus%2Ctrain%2Cboat&modes=bus&not_modes=bus%2Ctrain%2Cboat&not_modes=train&app_key={TRANSPORT_API_KEY}&app_id={TRANSPORT_APP_ID}'
        response = requests.get(api_url)
        data = response.json()
        print(data)# Assuming your API returns JSON data
        
        
        # Iterate through routes and find the highest-rated bus for each leg
        for route in data['routes']:
            for leg in route['route_parts']:
                route_duration = route['duration']

                if leg['mode'] == 'bus':
                    smscode = leg['from_point']['place']['smscode']
                    tolerance = 2
                    departure_time = leg['departure_time']

                    # Convert departure_time to a datetime.time object
                    departure_time = datetime.strptime(departure_time, '%H:%M').time()

                    # Calculate the time range
                    start_time = (datetime.combine(datetime.today(), departure_time) - timedelta(minutes=tolerance)).time()
                    end_time = (datetime.combine(datetime.today(), departure_time) + timedelta(minutes=tolerance)).time()
                    print(start_time, "", end_time)

                    average_rating = Review.objects.filter(bus_id=leg['line_name'], arrival_time__gte=start_time, arrival_time__lte=end_time, stop_point=smscode).aggregate(Avg('rating'))['rating__avg']
                    print(f"Rating: {average_rating}")
                    if average_rating is not None:
                     leg['suggested_bus'] = math.ceil(average_rating)
                    else:
                     leg['suggested_bus'] = None

        # Pass the data to the template for rendering
        return render(request, 'route_display.html', {'routes': data})

    else:
        # Handle the case where post codes were not found
        # You can print an error message or log it
        return render(request, 'error.html')

    return render(request, 'route_display.html')



def get_coordinates(postcode):
    # Use your Google Maps Geocoding API call to get coordinates
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={postcode}&key={COORDINATE_API_KEY}'

    response = requests.get(geocoding_url)
    data = response.json()
    if data['status'] == 'OK' and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']
        return location
    else:
        return None
    

    
    
def bus_detail(request):
    if request.method == 'GET':
        stop_name = request.GET.get('stop_name')
        bus_id = request.GET.get('bus_id')
        is_number = stop_name and stop_name[0].isdigit()
        
        if stop_name:
            if is_number:
                bus_info = BusRoute.objects.filter(stop_point=stop_name)
                buses = bus_info.values('bus_id').distinct()
                stop_name = stop_name
            else:
                bus_info = BusRoute.objects.filter(common_name=stop_name).values('bus_id').distinct()
                buses = bus_info.values('bus_id').distinct()
                stop_name_query = bus_info.values('stop_point').distinct()
                first_stop_name = stop_name_query.first()
                stop_name = first_stop_name.get('stop_point')
                
        else:
            buses = BusRoute.objects.none()
        print("Stop Name : ", stop_name)
        if bus_id:
            pickup = BusRoute.objects.filter(stop_point=stop_name, bus_id=bus_id).values('arrival_time').distinct().order_by('arrival_time')
            print(pickup)
        
            max_rating = Review.objects.filter(bus_id=bus_id, stop_point=stop_name).aggregate(Avg('rating'))['rating__avg']
            top_three_reviews = Review.objects.filter(bus_id=bus_id, stop_point=stop_name, comment__isnull=False,).exclude(comment__iexact='').order_by('-timestamp')[:3]
        else:
            max_rating = None
            top_three_reviews = None
            pickup = None
        
        return render(request, 'bus_detail.html', {
            
            'buses': buses,
            #'selected_bus': selected_bus,
            #'stop_point': stop_point,
            #'bus_providers': bus_providers,
            'max_rating': max_rating,
            'top_three_reviews': top_three_reviews,
            'pickups':pickup
            
        })

