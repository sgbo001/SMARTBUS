from django.shortcuts import render, redirect
from .forms import SearchForm
import requests
from django.http import HttpResponse
from datetime import datetime
from .models import Bus, BusRoute, Notification
from reviews.models import Review
from django.db.models import Avg, Max
from reviews.models import Review
import math
from datetime import datetime, timedelta
import os



transport_api_key = os.environ.get('TRANSPORT_API_KEY')
transport_app_id = os.environ.get('TRANSPORT_APP_ID')
coordinate_api_key = os.environ.get('COORDINATE_API_KEY')


    
def home(request):
   if request.user.is_authenticated:
        # User is signed in, redirect to 'route_plan'
        return redirect('route_plan')
   else:
        return render(request, 'home.html')
    
def error(request):

     return render(request, 'error.html')
 
def notifications(request):
    notifications = Notification.objects.all().order_by('-datetime')
    context = {'notifications': notifications}
    return render(request, 'notifications.html', context)

def notifications_count(request):
    count = Notification.objects.count()
    return render(request, 'base.html', {'notification_count': count})


def route_plan(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            from_post_code = form.cleaned_data['from_post_code']
            to_post_code = form.cleaned_data['to_post_code']
            date_time = form.cleaned_data['date_time']

    else:
        form = SearchForm()

    notification_count = Notification.objects.count()

    return render(request, 'route_plan.html', {'form': form, 'notification_count': notification_count})


def display_route(request):
    try:
        # Fetch data from the API
        from_post_code = request.GET.get('from_post_code')
        to_post_code = request.GET.get('to_post_code')

        from_post_code_info = get_coordinates(from_post_code, coordinate_api_key)
        to_post_code_info = get_coordinates(to_post_code, coordinate_api_key)

        if from_post_code_info and to_post_code_info:
            from_longitude = from_post_code_info['location']['lng']
            from_latitude = from_post_code_info['location']['lat']
            from_full_address = from_post_code_info['full_address']

            to_longitude = to_post_code_info['location']['lng']
            to_latitude = to_post_code_info['location']['lat']
            to_full_address = to_post_code_info['full_address']

            # Your code to call the API and display the results can go here
            # ...
            date_time_str = request.GET.get('date_time')
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
            date = date_time_obj.strftime('%Y-%m-%d')
            time = date_time_obj.strftime('%H:%M')

            api_url = f'https://transportapi.com/v3/uk/public_journey.json?from=lonlat%3A{from_longitude}%2C{from_latitude}&to=lonlat%3A{to_longitude}%2C{to_latitude}&date={date}&time={time}&journey_time_type=leave_after&service=silverrail&modes=bus%2Ctrain%2Cboat&modes=bus&not_modes=bus%2Ctrain%2Cboat&not_modes=train&app_key={transport_api_key}&app_id={transport_app_id}'
            response = requests.get(api_url)

            if response.status_code != 200:
                raise Http404

            data = response.json()

            # Iterate through routes and find the highest-rated bus for each leg
            for route in data.get('routes', []):
                for leg in route.get('route_parts', []):
                    route_duration = route.get('duration', 0)

                    if leg.get('mode') == 'bus':
                        smscode = leg['from_point']['place']['smscode']
                        tolerance = 2
                        departure_time = leg['departure_time']

                        # Convert departure_time to a datetime.time object
                        departure_time = datetime.strptime(departure_time, '%H:%M').time()

                        # Calculate the time range
                        start_time = (datetime.combine(datetime.today(), departure_time) - timedelta(minutes=tolerance)).time()
                        end_time = (datetime.combine(datetime.today(), departure_time) + timedelta(minutes=tolerance)).time()
                        print(start_time, "", end_time)

                        average_rating = Review.objects.filter(
                            bus_id=leg['line_name'],
                            arrival_time__gte=start_time,
                            arrival_time__lte=end_time,
                            stop_point=smscode
                        ).aggregate(Avg('rating'))['rating__avg']

                        print(f"Rating: {average_rating}")

                        if average_rating is not None:
                            leg['suggested_bus'] = math.ceil(average_rating)
                        else:
                            leg['suggested_bus'] = None

            # Pass the data to the template for rendering
            return render(request, 'route_display.html', {
                'from_full_address': from_full_address,
                'to_full_address': to_full_address,
                'routes': data
            })
        else:

            raise Http404
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'error.html')



def get_coordinates(postcode, coordinate_api_key):
    # Use your Google Maps Geocoding API call to get coordinates and address components
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={postcode}&key={coordinate_api_key}'

    response = requests.get(geocoding_url)
    data = response.json()

    if data['status'] == 'OK' and len(data['results']) > 0:
        location_result = data['results'][0]
        location = location_result['geometry']['location']
        full_address = location_result['formatted_address']

        return {
            'location': location,
            'full_address': full_address
        }
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
            'max_rating': max_rating,
            'top_three_reviews': top_three_reviews,
            'pickups':pickup
            
        })

