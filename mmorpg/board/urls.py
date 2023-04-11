from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
        responds, ResponseListView, ResponceListView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    # path('respond/<int:pk>', RespondCreateView.as_view(), name='respond_create'),
    path('responds/<int:pk>', responds, name='respond'),
    path('responses/', ResponceListView.as_view(), name='responses_list'),
]