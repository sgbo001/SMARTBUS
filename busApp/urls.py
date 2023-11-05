
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from bus.views import home, display_route, route_plan, bus_detail
from reviews.views import ReviewCreateView
from users import views as user_views
from django.contrib.auth import views as auth_views
from reviews import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('login', auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('register', user_views.register, name='register'),
    path('route_plan/', route_plan, name='route_plan'),
    path('bus_detail/', bus_detail, name='bus_detail'),
    path('route/', display_route, name='display_route'),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    #path('api/arrival_times/', views.get_arrival_times, name='get_arrival_times'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
