from typing import Iterable
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.common.models import BaseModel

from mutagen import File
from datetime import timedelta
from uuid import uuid4

from apps.users.models import User


class Category(BaseModel):
    name = models.CharField(max_length=255, help_text=_("Category name"))
    slug = models.SlugField(max_length=255, help_text=_("Category slug name"), editable=False)
    icon = models.ImageField(upload_to="categories_photo", help_text=_("Category icon"))

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Author(BaseModel):
    full_name = models.CharField(max_length=255, help_text=_("Author full name"))
    slug = models.SlugField(max_length=255, help_text=_("Author slug name"), editable=False)
    about = models.TextField(help_text=_("Author about"))

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.slug:
            self.slug = slugify(self.full_name)
        return super().save(*args, force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.full_name


def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = slugify(instance.title)
    unique_string = str(uuid4())[:6]
    return f'book_audio/{new_filename}_{unique_string}.{extension}'


class Book(BaseModel):
    title = models.CharField(max_length=255, unique=True, help_text=_("BookInfo name"))
    slug = models.SlugField(max_length=255, unique=True, editable=False, help_text=_("BookInfo slug name"))
    description = models.TextField(blank=True, null=True, help_text=_("BookInfo description"))
    like_count = models.PositiveIntegerField(default=0, help_text=_("BookInfo like_count"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    img = models.ImageField(upload_to="books_photo/", help_text=_("BookInfo image"))
    file = models.FileField(upload_to=upload_to, help_text=_("BookInfo audio. Only .mp3"))
    what_is_learned = models.JSONField(default=list, help_text=_("What is learned from the book"))
    duration = models.DurationField(help_text=_("BookInfo duration"), default=timedelta(seconds=0))
    is_premium = models.BooleanField(default=False)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, force_insert, force_update, using, update_fields)

        if self.file:
            try:
                file_path = self.file.path
                audio = File(file_path)

                if audio and audio.info:
                    duration_seconds = audio.info.length
                    self.duration = timedelta(seconds=duration_seconds)
                    self.save()

            except Exception as e:
                print(str(e))


    def __str__(self):
        return f"{self.title} - {self.author.full_name}"


class BookChapter(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    title = models.CharField(max_length=255, help_text=_("Chapter title"))
    chapter = models.TextField(help_text=_("Chapter description"))
    point = models.DurationField(help_text=_("Chapter point (seconds)"))

    class Meta:
        ordering = ["point"]

    def __str__(self):
        return f"{self.title} - {self.book.title}"


class UserBookRating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_ratings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} - {self.book.title}"


class BookSave(BaseModel):
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)

    def __str__(self):
        return f'{self.book.title} - {self.user.full_name}'


class Goal(BaseModel):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Collection(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='collection_images/', help_text=_("Collection image"))
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class UserStatistics(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goals = models.ManyToManyField(Goal)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.full_name


class Story(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="stories")
    title = models.CharField(max_length=255, help_text=_("Story title"))
    image = models.ImageField(upload_to="story_image/", help_text=_("Story image"))
    context = models.TextField(help_text=_("Story context"))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="stories", blank=True, null=True)

    def __str__(self):
        return self.title


class StoryUser(BaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    end_date = models.DateTimeField(editable=True, blank=True, null=True)

    def __str__(self):
        return f"{self.story.title} | {self.user.full_name}"


class StorySaveUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.full_name

