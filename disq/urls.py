import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('store.urls', namespace='store')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
                       path('__debug__/', include(debug_toolbar.urls)),
                   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
