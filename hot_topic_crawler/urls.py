from django.urls import path
from truthagent_back.hot_topic_crawler import views

urlpatterns = [
    path('crawl/hotlist', views.fetch_weibo_hot_topics, name='hot_topics'),
] 