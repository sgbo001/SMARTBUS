from django.shortcuts import render
from .forms import SearchForm
import requests
from django.http import HttpResponse
from datetime import datetime
from .models import PostCode, Bus
from reviews.models import Review
from django.db.models import Avg, Max
# Create your views here.

    
def home(request):
   
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

    # Search for longitude and latitude for from_post_code
    from_post_code_info = PostCode.objects.filter(post_code=from_post_code).first()

    # Search for longitude and latitude for to_post_code
    to_post_code_info = PostCode.objects.filter(post_code=to_post_code).first()

    if from_post_code_info and to_post_code_info:
        from_longitude = from_post_code_info.longitude
        from_latitude = from_post_code_info.latitude

        to_longitude = to_post_code_info.longitude
        to_latitude = to_post_code_info.latitude

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
                if leg['mode'] == 'bus':
                    highest_rated_bus = Review.objects.filter(bus_id__bus_id=leg['line_name']).aggregate(Max('rating'))['rating__max']
                    leg['suggested_bus'] = highest_rated_bus

        # Pass the data to the template for rendering
        return render(request, 'route_display.html', {'routes': data})

    else:
        # Handle the case where post codes were not found
        # You can print an error message or log it
        print("Invalid post codes")

    return render(request, 'route_display.html')



   