from django.conf.urls import patterns,url, include
from view import hello,login_home, test_template
from django.contrib import admin


urlpatterns = patterns(
                       url(r'^hello/$',hello),
                       url(r'^test$', test_template),
                       url(r'^tweet$', login_home),
                       url(r'^$', hello),
                       url(r'^admin/', include(admin.site.urls)),
)
