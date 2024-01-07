from django.test import TestCase
from django.utils import timezone
from .models import Review

class ReviewModelTest(TestCase):
    def test_review_defaults(self):
        # Test creating a review with default values
        new_review = Review.objects.create(
            full_name='John Doe',
            stop_point='Some Stop',
            bus_id='12345',
            rating=3,
            arrival_time=timezone.now(),
        )

        # Add assertions based on your model fields
        self.assertEqual(new_review.full_name, 'John Doe')
        self.assertEqual(new_review.stop_point, 'Some Stop')
        self.assertEqual(new_review.bus_id, '12345')
        self.assertEqual(new_review.rating, 3)
        self.assertIsNotNone(new_review.arrival_time)

    def test_review_rating_choices(self):
        # Test creating a review with a valid rating
        review = Review.objects.create(
            full_name='Jane Doe',
            stop_point='Another Stop',
            bus_id='67890',
            rating=3,
            arrival_time=timezone.now(),
        )

        # Add assertions based on your model fields
        self.assertEqual(review.full_name, 'Jane Doe')
        self.assertEqual(review.stop_point, 'Another Stop')
        self.assertEqual(review.bus_id, '67890')
        self.assertEqual(review.rating, 3)
        self.assertIsNotNone(review.arrival_time)

    # Add more test methods as needed
