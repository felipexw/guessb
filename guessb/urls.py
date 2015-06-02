from django.conf.urls import patterns, include, url
from django.contrib import admin
from guessb.view import show_home, show_posts, show_about, show_comentarios, show_posts_2

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
                       url(r'^home/$', show_home),
                       url(r'^posts/', show_posts_2),
                       url(r'^$', show_home),
                       url(r'^sobre/$', show_about),
                       url(r'^comments/$', show_comentarios),
)
