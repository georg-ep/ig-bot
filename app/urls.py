"""app URL Configuration"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include

from core.swagger import app_swagger_view

admin.site.site_header = 'Django default'
admin.site.index_title = 'Django default'
admin.site.site_title = 'Django default'
admin.site.site_url = ''

user_patterns = path('api/users/', include('user.urls'))
instagram_patterns = path('api/instagram/', include('instagram.urls'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(
        "docs/all/$",
        app_swagger_view(
            urls_patterns=(
                user_patterns,
                instagram_patterns,
                # Add documented patterns here
            ),
            title="User API"
        )
    ),
    instagram_patterns,
    user_patterns,
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
