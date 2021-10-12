"""Core URL routing for Django system."""

from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views import defaults as default_views
from rest_framework import routers
from programming.urls import router as programming_router
from research.urls import router as research_router
from users.urls import router as users_router

admin.site.login = login_required(admin.site.login)
admin.site.site_header = 'CodeWOF'

router = routers.DefaultRouter()
router.registry.extend(programming_router.registry)
router.registry.extend(research_router.registry)
router.registry.extend(users_router.registry)

urlpatterns = [
    path('', include('general.urls', namespace='general')),
    path(settings.ADMIN_URL, admin.site.urls),
    path('research/', include('research.urls', namespace='research')),
    path('style/', include('style.urls', namespace='style')),
    path('users/', include('users.urls', namespace='users'),),
    path('accounts/', include('allauth.urls')),
    path('', include('programming.urls', namespace='programming'),),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            '400/',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')},
        ),
        path(
            '403/',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')},
        ),
        path(
            '404/',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')},
        ),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
