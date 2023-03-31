class StageSender:
    def __init__(self, socketio):
        self.socketio = socketio

    def send_stage(self, stage_data):
        self.socketio.emit('process_stage', stage_data)