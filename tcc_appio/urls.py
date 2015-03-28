from django.conf.urls import patterns,url, include
from view import hello,login_home, home
from django.contrib import admin


urlpatterns = patterns(
                       url(r'^hello/$',hello),
                       url(r'^$', home),
                       url(r'^tweet$', login_home),
                       url(r'^$', hello),
                       url(r'^admin/', include(admin.site.urls)),
)
