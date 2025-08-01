from django import template
from dashboard.models import Notification

register = template.Library()

@register.inclusion_tag('dashboard/notifications/notification_list.html', takes_context=True)
def notifications(context):
    request = context.get('request')
    if request.user.is_authenticated and request.user.is_superuser:
        notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
        notifications_count = notifications.count()
        return {
            'notifications': notifications
            ,'notifications_count': notifications_count
        }
    else:
        return {}