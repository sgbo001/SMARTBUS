import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from reviews.models import Review
from datetime import time

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Make predictions using the trained model'

    def handle(self, *args, **kwargs):
        # Fetch relevant fields from the Review model
        bus_value = '52a'
        bus_check = Review.objects.filter(bus_id=bus_value)
        if bus_check.exists():
            print("Bus No", bus_value)
            
            reviews_data = Review.objects.values('bus_id', 'arrival_time', 'rating', 'stop_point')

            # Create a DataFrame from the queryset
            df = pd.DataFrame.from_records(reviews_data)

            # Convert 'arrival_time' to string format
            df['arrival_time'] = df['arrival_time'].apply(lambda x: x.strftime('%H:%M'))

            # Convert 'arrival_time' to datetime
            df['arrival_time'] = pd.to_datetime(df['arrival_time'], format='%H:%M')

            # Convert 'bus_id' to numerical values using label encoding
            label_encoder = LabelEncoder()
            df['bus_id'] = label_encoder.fit_transform(df['bus_id'])

            # One-hot encode 'stop_point'
            onehot_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
            stop_point_encoded = onehot_encoder.fit_transform(df['stop_point'].values.reshape(-1, 1))
            df_stop_point = pd.DataFrame(stop_point_encoded, columns=[f'stop_point_{int(i)}' for i in range(stop_point_encoded.shape[1])])
            df = pd.concat([df, df_stop_point], axis=1)

            # Convert 'arrival_time' to minutes
            df['arrival_minutes'] = df['arrival_time'].dt.hour * 60 + df['arrival_time'].dt.minute

            # Features and target variable
            X = df.drop(['rating', 'arrival_time', 'stop_point'], axis=1)
            y = df['rating']
            
            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
            new_data_bus_id = label_encoder.transform([bus_value])[0]
            # Use the same one-hot encoder for 'stop_point' as during training
            new_data_stop_point = onehot_encoder.transform([['37022803']])[0]
            new_data_arrival_minutes = 10 * 60 + 0

            new_data = pd.DataFrame({'bus_id': [new_data_bus_id],
                                    **dict(zip([f'stop_point_{int(i)}' for i in range(new_data_stop_point.shape[0])], new_data_stop_point)),
                                    'arrival_minutes': [new_data_arrival_minutes]
                                    })

            # Ensure the order of features is the same as during training
            new_data = new_data[X.columns]

            prediction = clf.predict(new_data)
            print(f"Predicted Rating: {prediction}")
        else:
            prediction = 0
            print(f"Predicted Rating: {prediction}")
        self.stdout.write(self.style.SUCCESS('Predictions made successfully'))
