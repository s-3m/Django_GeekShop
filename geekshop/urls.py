from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path, re_path
from mainapp import views as mainapp_views

"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

urlpatterns = [
    re_path(r'^$', mainapp_views.index, name='main'),
    re_path(r'^products/', include('mainapp.urls', namespace='products')),
    path('contact/', mainapp_views.contact, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    # path('admin/', admin.site.urls),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
