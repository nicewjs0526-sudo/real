from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Uppcoder has no separate web server in front of the container, so Django
    # serves uploaded media itself. Put large media on external storage instead.
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    ]
    if not getattr(settings, "HAS_WHITENOISE", False):
        urlpatterns += [
            re_path(
                r"^static/(?P<path>.*)$",
                serve,
                {"document_root": settings.STATIC_ROOT},
            )
        ]
