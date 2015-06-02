from django.conf.urls import patterns, include, url
from django.contrib import admin
from guessb.view import showComments, showPosts, showHome, showAbout

urlpatterns = patterns(url(r'^admin/', include(admin.site.urls)),
                       url(r'^home/$', showHome),
                       url(r'^posts/', showPosts),
                       url(r'^$', showHome),
                       url(r'^sobre/$', showAbout),
                       url(r'^comments/$', showComments),
)
