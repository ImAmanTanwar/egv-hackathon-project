from django.conf.urls import include, url
from django.contrib import admin
from hackproject import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'hackproject.views.test',name='test'),
    url(r'^api/', include('hack_api.urls')),
]
