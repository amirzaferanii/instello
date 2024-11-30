from django.urls import path
from . import views


app_name = 'profile'

urlpatterns = [
    path('profile/<slug:slug>', views.ProfileView.as_view(), name='home'),
    path('nav/', views.UserNavView.as_view(), name='nav'),
    path('', views.FeedView.as_view(), name='feed'),
    path('feed/follow/<slug:slug>', views.FeedFollowView.as_view(), name='feed-follow'),
    path('profile/follow/<slug:slug>', views.FollowInProfile.as_view(), name='follow-in-profile'),
    path('like/<int:pk>', views.LikePostView.as_view(), name='like_post'),
    path('postliker/<int:pk>', views.PostLiker.as_view(), name='post_liker'),
    path('comment/<int:id>', views.CommentView.as_view(), name='comment'),
    path('chat_create/<slug:slug>', views.ChatCreateView.as_view(), name='chat_create'),
    path('upload/', views.PostUpload.as_view(), name='upload_post'),
    path('delete/<int:id>', views.DeletePostView.as_view(), name='delete'),
    path('post/detail/<int:id>', views.PostDetailView.as_view(), name='post-detail'),
    path('like/detail/<int:pk>', views.LikePostInDetail.as_view(), name='like_detail'),
    path('comment/active/<int:id>', views.CommentActive.as_view(), name='comment_active'),
    path('user/following/<int:id>', views.Following.as_view(), name='user_following'),
    path('user/followers/<int:id>', views.Followers.as_view(), name='user_followers'),

]