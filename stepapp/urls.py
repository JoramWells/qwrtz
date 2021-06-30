from django.urls import path,include
from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static 
from .views import XmlViewset,index,PostViewSet,home,CsvViewSet,ProductViewset,ProductSearchViewset
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token


  
urlpatterns = [ 
    path('', index, name='index'),
    path('posts',XmlViewset.as_view({
        'get':'list',
    })),
    path('getDetail',PostViewSet.as_view({
    'post':'create',
    })),
    path('products',ProductViewset.as_view({
        'get':'list'
    })),
    path('product/search',ProductSearchViewset.as_view({
        'post':'create',
    })),
    path('recent/search',ProductSearchViewset.as_view({
        'get':'list',
    })),
    path("csv", CsvViewSet.as_view(), name="csv"),
    path('api/token/', obtain_auth_token, name="obtain-token"),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'))




] 

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
