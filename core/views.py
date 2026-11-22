import django
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    context = {
        "debug": settings.DEBUG,
        "django_version": django.get_version(),
        "db_vendor": connection.vendor,
    }
    return render(request, "core/index.html", context)


def status(request):
    """/health is answered by the Uppcoder platform, so use /status."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_ok = True
    except Exception:  # noqa: BLE001
        db_ok = False

    return JsonResponse(
        {
            "app": "ok",
            "database": "ok" if db_ok else "error",
            "vendor": connection.vendor,
        }
    )

