from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Post, Like
from django.forms.models import model_to_dict
from django.http import JsonResponse
from .forms import CommentsForm, PostsForm, RegisterUserForm


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            print(user)
            print('user register success')
            login(request, user)
            messages.success(request, ("Register success",))
            return redirect('index')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    post = Post.objects.all()
    return render(
        request,
        'post/index.html',
        {'post': post}
    )


class BlogDetail(DetailView, FormMixin):
    model = Post
    template_name = 'post/details_post.html'
    form_class = CommentsForm
    context_object_name = 'post'
    success_msg = 'success'

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'detail',
            kwargs={'pk': self.get_object().id}
        )

    # method post
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.name = self.request.user
        self.object.save()
        super().form_valid(form)
        return JsonResponse({'post': model_to_dict(self.object)}, status=200)


def blog_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.like_set.filter(
            user=request.user).exists():
        post.like_set.filter(
            user=request.user).delete()
    else:
        new = Like.objects.create(
            user=request.user, post=post)
        post.like_set.add(new)
    return JsonResponse({'likes_count': post.get_total_likes()}, status=200)


class DetailsAboutUser(DetailView):
    model = User
    template_name = 'post/user.html'
    context_object_name = 'user'

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'user',
            kwargs={'pk': self.get_object().id}
        )


def form_add_post(request):
    if request.method == 'POST':
        form = PostsForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            print('successfully add form')
    else:
        form = PostsForm()
    return render(request, 'post/add_new_post.html', {'form': form})
