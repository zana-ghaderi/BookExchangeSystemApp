from datetime import datetime


class Notification:
    def __init__(self, notification_id, user, message, notif_type, is_read=False):
        self.notification_id = notification_id
        self.user = user
        self.message = message
        self.notif_type = notif_type
        self.is_read = is_read
        self.created_at = datetime.now()

    def send_notification(self):
        # Code to send a notification to a user
        pass

    def mark_as_read(self):
        # Code to mark notification as read
        self.is_read = True

    @staticmethod
    def get_notifications(user_id):
        # Code to get all notifications for a user
        pass