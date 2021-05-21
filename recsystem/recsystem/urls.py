from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()
admin.site.enable_nav_sidebar = False
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('documentation/api/', TemplateView.as_view(template_name='redoc.html'), name='api'),
    path('', include('analytics.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)