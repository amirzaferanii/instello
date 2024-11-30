from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, View
from Account.models import User
from chatuser.models import Chat
from .forms import PostForm
from .models import Follow, Profile, Post, Like, Comment
from django.core.paginator import Paginator



class ProfileView(LoginRequiredMixin, View):
    def get(self, request, slug):
        is_followed = Follow.objects.filter(user=request.user).values_list('following__username', flat=True)
        user = get_object_or_404(User, slug=slug)
        profile = get_object_or_404(Profile, user=user)
        post_count = Profile.objects.filter(user=user, profile__user=user).count()
        posts = Post.objects.filter(user=user, profile__user=user)
        follow_record_profile = Follow.objects.get(user=user)
        followers = follow_record_profile.followers.count()
        following = follow_record_profile.following.count()
        context = {'profile': profile, 'user': user, 'followers': followers, 'following': following, 'post_counter': post_count, 'posts': posts, 'is_followed': is_followed}
        return render(request, 'Profile/profile.html', context)


class FollowInProfile(View):
    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        followed = Follow.objects.get(user=user)
        following = Follow.objects.get(user=request.user)
        if request.user in followed.followers.all():
            followed.followers.remove(request.user)
            following.following.remove(user)
        else:
            followed.followers.add(request.user)
            following.following.add(user)
        return redirect('profile:home', slug=slug)


class ChatCreateView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        chat = Chat.objects.filter(user1=request.user, user2=user).first() or Chat.objects.filter(user1=user, user2=request.user).first()
        if not chat:
            chat = Chat.objects.create(user1=request.user, user2=user)
        return redirect('chat_user:chat', chat.chat_id)



class UserNavView(View):
    def get(self, request):
        user_follow = request.user
        follow_record = Follow.objects.get(user=user_follow)
        follower = follow_record.followers.count()
        following = follow_record.following.count()
        profile = Profile.objects.get(user=user_follow)
        if user_follow.is_authenticated:
            context = {'follower': follower, 'following': following, 'profile': profile}
            return render(request, 'includes/user_navbar.html', context)



class FeedView(View):
    def get(self, request):
        if request.user.is_authenticated:
            users = Profile.objects.all().exclude(user=request.user)
            following_user = Follow.objects.filter(followers=request.user).values_list('user', flat=True)
            post_count = Post.objects.filter(user__in=following_user).count()
            posts = Post.objects.filter(user__in=following_user).prefetch_related('profile__user').order_by('-created')
            is_followed = Follow.objects.filter(user=request.user).values_list('following__id', flat=True)
            is_liked = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
            user_request_following = Follow.objects.filter(user=request.user).values_list('following', flat=True)
            users = users[:8]
            return render(request, 'Profile/feed.html', {'users': users, 'all_posts': posts, 'is_followed': is_followed,'is_liked': is_liked, 'user_request_following': user_request_following, 'post_count': post_count})
        else:
            return redirect('account:register')

class FeedFollowView(View):
    def post(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        followed = Follow.objects.get(user=user)
        following = Follow.objects.get(user=request.user)
        if request.user in followed.followers.all():
            followed.followers.remove(request.user)
            following.following.remove(user)
        else:
            followed.followers.add(request.user)
            following.following.add(user)
        return redirect('profile:feed')





class LikePostView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        profile = Profile.objects.get(user=request.user)
        user = request.user
        if Like.objects.filter(user=user, user_profile=profile, post=post).exists():
            Like.objects.filter(user=user, user_profile=profile, post=post).delete()
        else:
            Like.objects.create(user=user, user_profile=profile, post=post)
        return redirect("profile:feed")





class PostLiker(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        likers = Like.objects.filter(post=post).values_list('user', flat=True)
        profile = Profile.objects.filter(user__in=likers)
        context = {'post': post, 'profile': profile}
        return render(request, 'Profile/post_likers.html', context)






class CommentView(View):
    def get(self, request, id):
        post = Post.objects.get(comment_status=True, id=id)
        comments = Comment.objects.filter(post=post)
        context = {'comments': comments}
        return render(request, 'profile/comment.html', context)


    def post(self, request, id):
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        post = get_object_or_404(Post, id=id)
        Comment.objects.create(post=post, user=request.user, body=body, parent_id=parent_id)
        return redirect("profile:comment", post.id)





class PostUpload(View, LoginRequiredMixin):
    def get(self, request):
        form = PostForm()
        return render(request, 'Profile/post_upload.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        profile = Profile.objects.get(user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = profile
            post.save()
            return redirect('profile:feed')
        return render(request, 'Profile/post_upload.html', {'form': form})


class DeletePostView(View, LoginRequiredMixin):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect('profile:home', request.user.slug)




class PostDetailView(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        user = get_object_or_404(User, id=request.user.id)
        is_liked = Like.objects.filter(user=user).values_list('post_id', flat=True)
        user_request_following = Follow.objects.filter(user=request.user).values_list('following', flat=True)
        context = {'post': post, 'user_request_following': user_request_following, 'user': user, 'is_liked': is_liked}
        return render(request, 'Profile/post_details.html', context)




class LikePostInDetail(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        profile = Profile.objects.get(user=request.user)
        user = request.user
        if Like.objects.filter(user=user, user_profile=profile, post=post).exists():
            Like.objects.filter(user=user, user_profile=profile, post=post).delete()
        else:
            Like.objects.create(user=user, user_profile=profile, post=post)
        return redirect("profile:post-detail", post.id)



class CommentActive(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.comment_status == True:
            post.comment_status = False
            post.save()
        else:
            post.comment_status = True
            post.save()
        return redirect("profile:post-detail", post.id)



class Following(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        following = Follow.objects.filter(user=user).values_list('following', flat=True)
        profile = Profile.objects.filter(user__in=following)
        return render(request, 'Profile/followings.html', {"profile": profile})



class Followers(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        followers = Follow.objects.filter(user=user).values_list('followers', flat=True)
        profile = Profile.objects.filter(user__in=followers)
        return render(request, 'Profile/followers.html', {"profile": profile})