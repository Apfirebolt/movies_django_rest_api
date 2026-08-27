from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('admin/', admin.site.urls),
    path('editor/', include('django_summernote.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('my-blog/', include(('blog.urls', 'my-blog'), namespace='my-blog')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('api-schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Development-only static & media handlers
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += staticfiles_urlpatterns()