'''handles urls for the api'''
from django.urls import path
from . import views

#pylint: disable = C0103
app_name = 'api'
urlpatterns = [
    path('',views.index, name='index'),
    path('all/',views.all_blogs, name='blogs'),
    path('user_blogs/',views.user_blogs, name= 'user_blogs'),
    path('subscribers/',views.all_subscribers, name= 'subscribers'),
    path('get_blog/', views.get_blog, name = 'blog'),
    path('create/', views.post_blog,name='create_post'),
    path('register/', views.register_subscriber, name='register_subscriber'),
    path('delete/', views.delete_blog, name='delete'),
    path('register_user/', views.registration_view, name='register'),
    path('login/', views.custom_login, name= 'login'),
    path('logout/',views.logout_view, name='logout'),
    path('latest/',views.get_latest_blogs, name='latest'),
    path('latest_blog/', views.get_latest_blog, name='latest_blog'),
    path('statistics/', views.get_statistics, name='statistics'),
    path('viewed/', views.count_views, name='viewed'),
    path('like/', views.count_likes, name='like'),
    path('dislike/', views.count_dislikes, name='dislike'),
]
