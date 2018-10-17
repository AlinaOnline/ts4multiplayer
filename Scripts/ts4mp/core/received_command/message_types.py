class ProtocolBufferMessage:
    def __init__(self, msg_id, msg):
        self.msg_id = msg_id
        self.msg = msg

class HeartbeatMessage:
    def __init__(self, sent_time):
        self.sent_time = sent_time
