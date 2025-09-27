
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from application import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription/', views.inscription, name='inscription'),
    path('', views.connexion, name='connexion'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    
    # path('',include('application.urls')) ,
    path('', include('application.urls', namespace='application')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

