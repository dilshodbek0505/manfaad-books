from apps.notification.utils import send_push_notification
from core.celery import app
from apps.notification.models import NotificationUser, UserFCMToken, Notification


@app.task(queue="notification")
def send_notification(user_notifications_ids: list, notification_id: str) -> str:
    print("saa")
    notification = Notification.objects.get(id=notification_id)
    user_notification_ids=NotificationUser.objects.filter(id__in=user_notifications_ids).values_list('user', flat=True)
    user_tokens = UserFCMToken.objects.filter(user__in=user_notification_ids)
    print("aaaa")
    for user_token in user_tokens:
        print("keetii")
        send_push_notification(token=user_token.token, title=notification.title, message=notification.message)
        print("tugadi")

    return 'success'
