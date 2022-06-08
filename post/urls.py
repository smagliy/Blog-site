from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('', views.index, name='index'),
    path('<int:pk>', views.BlogDetail.as_view(), name='detail'),
    path('blog-like/<int:pk>', views.blog_like, name='blogpost_like'),
    path('deatils-user/<int:pk>', views.DetailsAboutUser.as_view(), name='user'),
    path('add_new_user/', views.form_add_post, name='add_new_post'),
]
