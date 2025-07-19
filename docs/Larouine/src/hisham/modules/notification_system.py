class NotificationSystem:
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, callback):
        self.subscribers.append(callback)
    
    def notify(self, event_type: str, message: str):
        for sub in self.subscribers:
            sub({
                'type': event_type,
                'message': message,
                'timestamp': time.time()
            })
    
    def send_alert(self, message: str):
        self.notify('ALERT', message)
    
    def send_info(self, message: str):
        self.notify('INFO', message)