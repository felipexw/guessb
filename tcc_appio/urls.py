from django.conf.urls import patterns,url, include
from view import get_comentarios, show_home, show_posts, show_paginacao
from django.contrib import admin


urlpatterns = patterns(
                       url(r'^home/$', show_home),
                       url(r'^home/$', show_home),
                       url(r'^posts/', show_posts),
                       url(r'^$', show_home),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^paginacao/$', show_paginacao),                       
)
