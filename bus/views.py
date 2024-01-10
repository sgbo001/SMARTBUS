from django.shortcuts import render, redirect
from .forms import SearchForm
import requests
from django.http import Http404, HttpResponse
from datetime import datetime
from .models import Bus, BusRoute, Notification
from reviews.models import Review
from django.db.models import Avg, Max
from reviews.models import Review
import math
from datetime import datetime, timedelta
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder



transport_api_key = os.environ.get('TRANSPORT_API_KEY')
transport_app_id = os.environ.get('TRANSPORT_APP_ID')
coordinate_api_key = os.environ.get('COORDINATE_API_KEY')


def get_started(request):

     return render(request, 'get_started.html')
    
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
                        departure_time = leg['departure_time']
                        departure_time1 = datetime.strptime(departure_time, '%H:%M').time()
                        departure_hours = departure_time1.hour
                        departure_minutes = departure_time1.minute

                        # Now you can use departure_hours and departure_minutes as needed
                        print(f"Departure Hours: {departure_hours}, Departure Minutes: {departure_minutes}")
                        bus_check = Review.objects.filter(bus_id=leg['line_name'], stop_point=smscode)
                        if bus_check.exists():
                        # Convert departure_time to a datetime.time object
                            departure_time = datetime.strptime(departure_time, '%H:%M').time()

                            reviews_data = Review.objects.values('bus_id', 'arrival_time', 'rating', 'stop_point')

                            df = pd.DataFrame.from_records(reviews_data)

                            # Convert 'arrival_time' to string format
                            df['arrival_time'] = df['arrival_time'].apply(lambda x: x.strftime('%H:%M'))

                            # Convert 'arrival_time' to datetime
                            df['arrival_time'] = pd.to_datetime(df['arrival_time'], format='%H:%M')

                            # Convert 'bus_id' to numerical values using label encoding
                            label_encoder = LabelEncoder()
                            df['bus_id'] = label_encoder.fit_transform(df['bus_id'])

                            # One-hot encode 'stop_point'
                            onehot_encoder = OneHotEncoder(sparse=False)
                            stop_point_encoded = onehot_encoder.fit_transform(df['stop_point'].values.reshape(-1, 1))
                            df_stop_point = pd.DataFrame(stop_point_encoded, columns=[f'stop_point_{int(i)}' for i in range(stop_point_encoded.shape[1])])
                            df = pd.concat([df, df_stop_point], axis=1)

                            # Convert 'arrival_time' to minutes
                            df['arrival_minutes'] = df['arrival_time'].dt.hour * 60 + df['arrival_time'].dt.minute

                            # Features and target variable
                            X = df.drop(['rating', 'arrival_time', 'stop_point'], axis=1)
                            y = df['rating']

                            # Split the data into training and testing sets
                        # Split the data into training and testing sets
                            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

                            # Initialize the RandomForestClassifier
                            clf = RandomForestClassifier(n_estimators=100, random_state=42)

                            # Fit the classifier on the training data
                            clf.fit(X_train, y_train)

                            # Make predictions on the testing data
                            predictions = clf.predict(X_test)

                            # Evaluate the accuracy of the model
                            accuracy = accuracy_score(y_test, predictions)
                            print(f"Model Accuracy: {accuracy}")

                            # Now, you can use the trained model to predict the likelihood for new data
                            new_data_bus_id = label_encoder.transform([leg['line_name']])[0]
                            new_data_stop_point = onehot_encoder.transform([[smscode]])[0]  # Replace 'your_stop_point' with the actual stop point
                            new_data_arrival_minutes = departure_hours * 60 + departure_minutes

                            new_data = pd.DataFrame({'bus_id': [new_data_bus_id],
                                                    **dict(zip([f'stop_point_{int(i)}' for i in range(new_data_stop_point.shape[0])], new_data_stop_point)),
                                                    'arrival_minutes': [new_data_arrival_minutes]
                                                    })

                            # Ensure the order of features is the same as during training
                            new_data = new_data[X.columns]

                            # Predict using the trained model
                            prediction = clf.predict(new_data)
                            leg['suggested_bus'] = prediction[0]
                            print(f"Predicted Rating: {leg['suggested_bus']}")
                        else:
                            leg['suggested_bus'] = 0
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
        arrival_time = request.GET.get('arrival_time')
        
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
        
        print("Stop Name:", stop_name)
        rating = 0
        
        if bus_id:
            pickup = BusRoute.objects.filter(stop_point=stop_name, bus_id=bus_id).values('arrival_time').distinct().order_by('arrival_time')
            arrival_time = Review.objects.filter(stop_point=stop_name, bus_id=bus_id).values('arrival_time').distinct().order_by('arrival_time')
            print(pickup)
        
            top_three_reviews = Review.objects.filter(bus_id=bus_id, stop_point=stop_name, comment__isnull=False).exclude(comment__iexact='').order_by('-timestamp')[:3]
        else:
        
            top_three_reviews = None
            pickup = None
            
        if bus_id and request.GET.get('arrival_time'):
            arrival_time_str = str(request.GET.get('arrival_time'))
            print(f"Departure Hours: {arrival_time_str}")
            hour_minute_parts = arrival_time_str.split(':')
            if len(hour_minute_parts) >= 2:
                hour = hour_minute_parts[0]
                minute = hour_minute_parts[1].split()[0]  # Removing any additional characters after the minute
                print(f"Hour: {hour}, Minute: {minute}")
            else:
                hour = hour_minute_parts[0]
                minute = 0
                print("Invalid time format")
            
            bus_value = bus_id  
            bus_check = Review.objects.filter(bus_id=bus_value, stop_point=stop_name)
            
            if bus_check.exists():
                print("Bus No", bus_value)
                
                reviews_data = Review.objects.values('bus_id', 'arrival_time', 'rating', 'stop_point')
                df = pd.DataFrame.from_records(reviews_data)
                
                df['arrival_time'] = df['arrival_time'].apply(lambda x: x.strftime('%H:%M'))
                df['arrival_time'] = pd.to_datetime(df['arrival_time'], format='%H:%M')
                
                label_encoder = LabelEncoder()
                df['bus_id'] = label_encoder.fit_transform(df['bus_id'])
                
                onehot_encoder = OneHotEncoder(sparse=False)
                stop_point_encoded = onehot_encoder.fit_transform(df['stop_point'].values.reshape(-1, 1))
                df_stop_point = pd.DataFrame(stop_point_encoded, columns=[f'stop_point_{int(i)}' for i in range(stop_point_encoded.shape[1])])
                df = pd.concat([df, df_stop_point], axis=1)
                
                df['arrival_minutes'] = df['arrival_time'].dt.hour * 60 + df['arrival_time'].dt.minute
                
                X = df.drop(['rating', 'arrival_time', 'stop_point'], axis=1)
                y = df['rating']
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
                
                clf = RandomForestClassifier(n_estimators=100, random_state=42)
                clf.fit(X_train, y_train)
                
                predictions = clf.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                print(f"Model Accuracy: {accuracy}")
                print("Stop Name : " , stop_name)
                new_data_bus_id = label_encoder.transform([bus_value])[0]
                new_data_stop_point = onehot_encoder.transform([[stop_name]])[0]
                new_data_arrival_minutes = int(hour) * 60 + int(minute)
                
                new_data = pd.DataFrame({'bus_id': [new_data_bus_id],
                                        **dict(zip([f'stop_point_{int(i)}' for i in range(new_data_stop_point.shape[0])], new_data_stop_point)),
                                        'arrival_minutes': [new_data_arrival_minutes]
                                        })
                
                new_data = new_data[X.columns]
                
                prediction = clf.predict(new_data)
                print(f"Predicted Rating: {prediction}")
                rating = prediction[0]
            else:
                prediction = 0
                print(f"Predicted Rating: {prediction}")
                rating = prediction
        
        return render(request, 'bus_detail.html', {
            'buses': buses,
            'top_three_reviews': top_three_reviews,
            'pickups': pickup,
            'rating': rating,
            'arrival_times': arrival_time
        })

