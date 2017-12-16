from django.conf.urls import url
import views

urlpatterns = [
    url(r'^send/$', views.send,{},name="send"),
    url(r'^view/$', views.view,{},name="view"),
]
