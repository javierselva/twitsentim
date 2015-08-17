from django.conf.urls import url

from . import views

'''
This file contains the url patterns so the server knows where
to redirect everytime a concrete url is requested.
This file should be imported to the main aplication urls.py
in order for everything to work.
'''

urlpatterns = [
    # /tweetclass/
    url(r'^$',views.index,name='index'),
    # /tweetclass/query_page/
    url(r'^query_page/$', views.query_page,name='query_page'),
    # /tweetclass/whats_this/
    url(r'^whats_this/$', views.whats_this,name='whats_this'),
    # /tweetclass/34/show_results/
    url(r'^(?P<requested_query_data_id>[0-9]+)/show_results/$', views.show_results,name='show_results'),
    # /tweetclass/42/show_historic/
    url(r'^(?P<requested_query_data_id>[0-9]+)/show_historic/$', views.show_historic,name='show_historic'),
    # /tweetclass/add_test/
    url(r'^add_test/$', views.add_test,name='add_test'),
]
