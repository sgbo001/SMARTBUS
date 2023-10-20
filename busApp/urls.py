
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from bus.views import home
from reviews.views import ReviewCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
