from django.db.models import QuerySet
from socialmedia.blog.models import Post , Subcription
from socialmedia.users.models import BaseUser
from socialmedia.blog.filters import PostFilter

def get_subscribers(* , user:BaseUser) -> QuerySet[Subcription]:
    return Subcription.objects.filter(subscriber = user)

def post_detail(* , slug:str , user:BaseUser , self_include:bool = True) -> Post:
    subscribtions = list(Subcription.objects.filter(subscriber = user).values_list("target" , flat=True))
    if self_include:
        subscribtions.append(user.id)
    return Post.objects.get(slug = slug , author__in = subscribtions)

def post_list(* , filters= None , user:BaseUser , self_include:bool = True):
    filters = filters or {}
    subscribtions = list(Subcription.objects.filter(subscriber= user).values_list("target" , flat=True))
    if self_include:
        subscribtions.append(user.id)
    if subscribtions:
        qs = Post.objects.filter(author__in  = subscribtions)
        return PostFilter(filters , qs).filters
    return Post.objects.none()


