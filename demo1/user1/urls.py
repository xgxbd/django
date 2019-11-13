from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),
    url(r'^get_body$', views.get_body),
    url(r'^no_form$', views.no_form),
    url(r'^information$', views.information),
    url(r'^page$', views.page),
    url(r'^mark$', views.mark),
    url(r'^mark1$', views.mark1),
     url(r'^DemoView$', views.DemoView.as_view()), # 7. # 这里的调用其实是函数调用
]   # 相当于 views.DemoView.as_view()()，views.DemoView.as_view() 返回的是，装饰器内层函数的地址，然后wrapper（）调用


