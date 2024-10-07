from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.book.models import UserBookRating, Story, StoryUser
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
        story_objects = [
            StoryUser(user=user, story=instance) for user in users
        ]
        StoryUser.objects.bulk_create(story_objects)


@receiver(post_save, sender=User)
def create_user_for_stories(sender, instance, created, **kwargs):
    if created:
        stories = Story.objects.all()
        story_objects = [
            StoryUser(user=instance, story=story) for story in stories
        ]
        StoryUser.objects.bulk_create(story_objects)







