from django.urls import path, include

urlpatterns = [
    path('blog/', include(('socialmedia.blog.urls', 'blog'))),
    path('user/', include(('socialmedia.users.urls', 'users'))),
    path('auth/', include(('socialmedia.authentication.urls', 'auth'))),
]
