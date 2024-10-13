from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

#router
urlpatterns = [
    path('', views.getHome, name="getHome"),
    path('about/', views.about, name='about'),
    path('comment/', views.comment_view, name='comment_view'),
    #path('comment/', views.comment_page, name='comment_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



