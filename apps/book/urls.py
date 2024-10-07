from django.urls import path

from apps.book.api_endpoints.BookInfo.views import (
    BookWithGenerateAudioUrl,
    BookWithoutGenerateAudioUrl
)
from apps.book.api_endpoints.HomePage.views import (
    HomePage,
)
from apps.book.api_endpoints.BookSave.views import (
    BookSaveApi,
    BookSaveListApi
)
from apps.book.api_endpoints.Search.views import (
    SearchHomeApi,
    SearchDataApi
)
from apps.book.api_endpoints.Story.views import (
    StoryListApi,
    StoryUpdateApi
)


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
]
