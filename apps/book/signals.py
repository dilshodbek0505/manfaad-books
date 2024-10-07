from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from apps.book.models import UserBookRating, Story, StoryUser, Book
from apps.users.models import User


@receiver(post_save, sender=UserBookRating)
def create_book_rating(sender, instance, created, **kwargs):
    like_count = UserBookRating.objects.filter(book=instance.book, is_liked=True).count()
    instance.book.like_count = like_count
    instance.book.save()


@receiver(post_save, sender=Story)
def create_story_for_users(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        end_time = timezone.now() + timezone.timedelta(minutes=4)
        story_objects = [
            StoryUser(user=user, story=instance, end_date=end_time) for user in users
        ]
        StoryUser.objects.bulk_create(story_objects)


@receiver(post_save, sender=User)
def create_user_for_stories(sender, instance, created, **kwargs):
    if created:
        stories = Story.objects.all()
        end_time = timezone.now() + timezone.timedelta(minutes=4)
        story_objects = [
            StoryUser(user=instance, story=story, end_date=end_time) for story in stories
        ]
        StoryUser.objects.bulk_create(story_objects)


@receiver(post_save, sender=Book)
def create_user_book(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        user_book_ratings = [UserBookRating(user=user, book=instance) for user in users]
        user_book_rating_objs = UserBookRating.objects.bulk_create(user_book_ratings)
    



        




