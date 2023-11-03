from django.shortcuts import render, redirect
from .forms import SearchForm
import requests
from django.http import HttpResponse
from datetime import datetime
from .models import Bus
from reviews.models import Review
from django.db.models import Avg, Max
from reviews.models import Review
import math
from datetime import datetime, timedelta
# Create your views here.

    
def home(request):
   if request.user.is_authenticated:
        # User is signed in, redirect to 'route_plan'
        return redirect('route_plan')
   else:
        return render(request, 'home.html')

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

        api_url = f'https://transportapi.com/v3/uk/public_journey.json?from=lonlat%3A{from_longitude}%2C{from_latitude}&to=lonlat%3A{to_longitude}%2C{to_latitude}&date={date}&time={time}&journey_time_type=leave_after&service=silverrail&modes=bus%2Ctrain%2Cboat&modes=bus&not_modes=bus%2Ctrain%2Cboat&not_modes=train&app_key=b0172443d13086192192fc659ac988ef&app_id=b42e95c3'
        response = requests.get(api_url)
        data = response.json()  # Assuming your API returns JSON data
        
        
        # Iterate through routes and find the highest-rated bus for each leg
        for route in data['routes']:
            for leg in route['route_parts']:
                route_duration = route['duration']
                print(f"Route Duration: {route_duration}")
                if leg['mode'] == 'bus':
                    smscode = leg['from_point']['place']['smscode']
                    average_rating = Review.objects.filter(bus_id__bus_id=leg['line_name'], stop_point__stop_point=smscode).aggregate(Avg('rating'))['rating__avg']
                    if average_rating is not None:
                     leg['suggested_bus'] = math.ceil(average_rating)
                    else:
                     leg['suggested_bus'] = None

        # Pass the data to the template for rendering
        return render(request, 'route_display.html', {'routes': data})

    else:
        # Handle the case where post codes were not found
        # You can print an error message or log it
        print("Invalid post codes")

    return render(request, 'route_display.html')



def get_coordinates(postcode):
    # Use your Google Maps Geocoding API call to get coordinates
    api_key = 'AIzaSyBic5uX0v4MzK_HoMYlw03cbUvV7lev1Yk'  # Replace with your Google Maps API key
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={postcode}&key={api_key}'

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
        
        
        if stop_name:
            buses = Bus.objects.filter(stop_points__stop_point=stop_name)
        else:
            buses = Bus.objects.none()
        
        if bus_id:
            selected_bus = Bus.objects.get(bus_id=bus_id)
            stop_point = selected_bus.stop_points.first()
            bus_providers = selected_bus.bus_providers.all()
            max_rating = Review.objects.filter(bus_id=selected_bus, stop_point=stop_point).aggregate(Max('rating'))['rating__max']
            top_three_reviews = Review.objects.filter(bus_id=selected_bus, stop_point=stop_point, comment__isnull=False,).exclude(comment__iexact='').order_by('-timestamp')[:3]
            print(selected_bus)
            print(stop_point)
            print(bus_providers)
            print(max_rating)
            print(top_three_reviews)
        else:
            selected_bus = None
            stop_point = None
            bus_providers = None
            max_rating = None
            top_three_reviews = None
        
        return render(request, 'bus_detail.html', {
            
            'buses': buses,
            'selected_bus': selected_bus,
            'stop_point': stop_point,
            'bus_providers': bus_providers,
            'max_rating': max_rating,
            'top_three_reviews': top_three_reviews
            
            
        })


