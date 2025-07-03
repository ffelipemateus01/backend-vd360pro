from api.io.cameras.recorder import VideoRecorder

video_recorder = VideoRecorder()

def init_camera(device_name: str, device_id: int):
    video_recorder.set_camera(camera_id=device_name, device_index=device_id)