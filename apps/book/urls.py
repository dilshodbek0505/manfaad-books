from django.urls import path
from apps.book.api_endpoints import *
from apps.book.api_endpoints.Goal import GoalListAPIView

app_name = "book"


urlpatterns = [
    path('book-details/<uuid:book_id>/', BookWithGenerateAudioUrl.as_view()),
    path('book-audio/<uuid:book_id>/<str:book_url>/<uuid:user_id>/', BookWithoutGenerateAudioUrl.as_view()),

    # home page api
    path('home/', HomePage.as_view()),

    # book save
    path('book-details/<uuid:pk>/save/', BookSaveApi.as_view()),
    path('book-details/save/books/', BookSaveListApi.as_view()),

    # search
    path('search/', SearchHomeApi.as_view()),
    path('search/book/', SearchDataApi.as_view()),

    # story
    path('story/', StoryListApi.as_view()),
    path('story-details/<uuid:pk>/', StoryUpdateApi.as_view()),
    path('story-save/', StorySaveUserListCreateApi.as_view()),
    path('story-save/<uuid:pk>/', StorySaveUserDeleteApi.as_view()),

    # liked
    path('book-user-like/list/', BookLikedListApi.as_view()),
    path('book-user-like/details/<uuid:pk>/', BookLikedUpdateApi.as_view()),

    path('category/list/', CategoryListAPIView.as_view(), name='category-list'),
    path('goal/list/', GoalListAPIView.as_view(), name='goal-list'),

]
