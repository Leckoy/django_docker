
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  
from cook.views import *
from project import settings

urlpatterns = [
    path('', include("first_page.urls")),
    path('cook/', include('cook.urls')),
	path("student/", include("student.urls")),
	path("start/", include("main.urls")),
	path("canadmin/", include("canadmin.urls"))

]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)