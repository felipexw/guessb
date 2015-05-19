from django.conf.urls import patterns, url, include
from view import get_comentarios, show_home, show_posts, show_about
from django.contrib import admin


urlpatterns = patterns(
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^home/$', show_home),
                       url(r'^posts/', show_posts),
                       url(r'^$', show_home),
                       url(r'^sobre/$', show_about),
                       url(r'^comments/$', get_comentarios),                                              
)

