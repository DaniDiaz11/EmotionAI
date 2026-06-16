from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MensajeViewSet


router = DefaultRouter()

router.register(
    r'mensajes',
    MensajeViewSet,
    basename='mensaje'
    
)

urlpatterns = [
    
    path('', include(router.urls)),
]
