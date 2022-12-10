"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.urls import path
from .views import TutorialViewSet, TagViewSet, CategoryViewSet

tutorial_list = TutorialViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
tutorial_detail = TutorialViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tag_list = TagViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
tag_detail = TagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

cat_list = CategoryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
cat_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', views.index, name='index'),
    path('tutorials', views.tutorials, name='tutorials'),
    path('single_tutorial/<int:pk>/', views.single_tutorial, name='single_tutorial'),

    path('tutorials_list/', tutorial_list, name='tutorials_list'),
    path('tutorials/<int:pk>/', tutorial_detail, name='tutorial-detail'),

    path('tags/', tag_list, name='tag-list'),
    path('tags/<int:pk>/', tag_detail, name='tag-detail'),

    path('cats/', cat_list, name='cat_list'),
    path('cats/<int:pk>/', cat_detail, name='cat-detail'),

]
