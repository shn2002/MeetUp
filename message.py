class Message:
    def __init__(self, sender_id=-1, recipient_id=-1, content=''):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content
        self.id = -1
        self.sent_Time = ""

    def render(self):
        return self.content

    def get_message(self):
        return self.sender_id, self.recipient_id, self.content


class UnderlineWarpper(Message):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return "<u>{}</u>".format(self._wrapped.render())


class BoldWrapper(Message):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return "<b>{}</b>".format(self._wrapped.render())