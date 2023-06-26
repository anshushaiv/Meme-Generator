from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('upload/', user_uploads, name='user_uploads' ),
    path('customise/<int:id>/<str:slug>/', customise, name="customise"),
    path('generate/<int:id>/<str:slug>/', generate, name="generate"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
