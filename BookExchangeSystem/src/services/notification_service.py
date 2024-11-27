class NotificationService:
    def __init__(self):
        self.notifications = {}

    def send_notification(self, notification) -> None:
        self.notifications[notification.notification_id] = notification

    def get_user_notifications(self, user_id):
        return [notification for notification in self.notifications.values() if notification.recipient.id == user_id]

    def mark_notification_as_read(self, notification_id) -> None:
        notification = self.notifications[notification_id]
        if notification:
            notification.is_read = True