from django.conf.urls import patterns,url, include
from view import hello,login_home, home, get_comentarios
from django.contrib import admin


urlpatterns = patterns(
                       url(r'^hello/$',hello),
                       url(r'^$', home),
                       url(r'^tweet$', login_home),
                       url(r'^$', hello),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^comentarios', get_comentarios),
)
