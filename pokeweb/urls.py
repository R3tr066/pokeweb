from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cards/', views.cards_list, name='cards_list'),
    path('cards/<str:card_id>/', views.card_detail, name='card_detail'),
    path('sets/', views.sets_list, name='sets_list'),
    path('sets/<str:set_id>/', views.set_detail, name='set_detail'),
    
    # API endpoints
    path('api/cards/search/', views.api_search_cards, name='api_search_cards'),
    path('api/cards/<str:card_id>/', views.api_card_detail, name='api_card_detail'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)