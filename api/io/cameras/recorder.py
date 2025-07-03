import cv2
import numpy as np
import threading
import time
import json
import struct
from api.io.cameras.tracker import PupilTracker
from fastapi import WebSocket
import asyncio

class VideoRecorder():
    def __init__(self, video_path="output.mp4", frame_size=(640, 480), fps=25.0):
        super().__init__()
        self.pupil_lock = threading.Lock()
        self.video_path = video_path
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(video_path, self.fourcc, fps, frame_size)
        self.recording = False
        self.running = True
        self.frames_to_send = []
        self.cameras = {}  # Dicionário de câmeras: {camera_id: cv2.VideoCapture}
        self.last_pupils = {}  # Dicionário de pupilas: {camera_id: [x, y, r]}
        self.watermark = cv2.imread("api/io/cameras/images/logoNeurograff.png", cv2.IMREAD_UNCHANGED)
        self.frame_size = frame_size
        self.pupil_tracker = PupilTracker()
        self.prepare_watermark()
        self.websocket = None  # Referência ao WebSocket

        if not self.out.isOpened():
            print("Erro ao abrir o arquivo de vídeo!")
            self.running = False

    def prepare_watermark(self):
        if self.watermark is None:
            return
        wm_scale = 0.13
        wm_width = int(self.frame_size[0] * (wm_scale + 0.23))
        wm_height = int(self.frame_size[1] * wm_scale)
        self.watermark_resized = cv2.resize(self.watermark, (wm_width, wm_height))
        if self.watermark_resized.shape[2] == 4:
            wm_b, wm_g, wm_r, alpha = cv2.split(self.watermark_resized)
            self.watermark_rgb = cv2.merge([wm_b, wm_g, wm_r])
            self.alpha = alpha / 255.0
        else:
            self.watermark_rgb = self.watermark_resized
            self.alpha = np.ones(self.watermark_rgb.shape[:2], dtype=np.uint8) / 255.0

    def apply_watermark(self, frame):
        if self.watermark_rgb is None:
            return frame
        frame_height, frame_width = frame.shape[:2]
        wm_height, wm_width = self.watermark_rgb.shape[:2]
        x_offset = frame_width - wm_width - 10
        y_offset = frame_height - wm_height - 10
        if x_offset < 0 or y_offset < 0:
            return frame
        roi = frame[y_offset:y_offset+wm_height, x_offset:x_offset+wm_width]
        alpha = self.alpha[..., np.newaxis]
        result = (roi * (1 - alpha) + self.watermark_rgb * alpha).astype(np.uint8)
        frame[y_offset:y_offset+wm_height, x_offset:x_offset+wm_width] = result
        return frame

    def get_frame_or_placeholder(self, cap, last_pupil, camera_id):
        if cap is None or not cap.isOpened():
            return None, last_pupil
        ret, frame = cap.read()
        if not ret:
            return None, last_pupil
        frame = cv2.resize(frame, self.frame_size)
        pupil = self.pupil_tracker.detect_pupil(frame)
        if pupil is not None:
            self.last_pupils[camera_id] = pupil
        return frame, self.last_pupils.get(camera_id)

    def draw_pupil(self, frame, pupil):
        if pupil is not None and len(pupil) == 3:
            x, y, radius = map(int, pupil)
            # Desenhar um círculo verde para a pupila
            cv2.circle(frame, (x, y), radius, (180, 130, 70), -1)
            cv2.circle(frame, (x, y), 3, (0, 0, 0), -1)
        return frame

    async def send_frame(self, frame, camera_id, pupil):
        try:
            if self.websocket is None:
                return
            with self.pupil_lock:
                pupil_data = [int(pupil[0]), int(pupil[1]), int(pupil[2])] if pupil else [-1, -1, -1]
                pupil_json = json.dumps({"pupil": pupil_data}).encode('utf-8')
                if len(pupil_json) == 0:
                    print(f"Erro: JSON da pupila vazio para câmera {camera_id}")
                    return
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                frame_data = buffer.tobytes()
                print(f"Enviando frame da câmera {camera_id}: JSON size={len(pupil_json)}, Image size={len(frame_data)}")
                await self.websocket.send_bytes(
                    struct.pack('B', camera_id) +
                    struct.pack('I', len(pupil_json)) + pupil_json +
                    struct.pack('I', len(frame_data)) + frame_data
                )
                print(f"Frame da câmera {camera_id} enviado com sucesso")
        except Exception as e:
            print(f"Erro ao enviar frame da câmera {camera_id}: {e}")

    async def run(self, websocket: WebSocket):
        self.websocket = websocket
        frame_interval = 1.0 / 25.0

        while self.running:
            start_time = time.time()

            with self.pupil_lock:
                camera_ids = list(self.cameras.keys())

            if not camera_ids:
                await asyncio.sleep(0.1)
                continue

            for camera_id in camera_ids:
                with self.pupil_lock:
                    cap = self.cameras.get(camera_id)
                if cap is None:
                    continue

                frame, pupil = self.get_frame_or_placeholder(cap, self.last_pupils.get(camera_id), camera_id)
                if frame is not None:
                    frame = self.draw_pupil(frame, pupil)
                    processed_frame = self.apply_watermark(frame)
                    if self.recording:
                        self.out.write(processed_frame)
                    await self.send_frame(processed_frame, camera_id, pupil)

            elapsed_time = time.time() - start_time
            sleep_time = frame_interval - elapsed_time
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
    
    def set_camera(self, camera_id, device_index):
        with self.pupil_lock:
            if device_index >= 0:
                if camera_id in self.cameras:
                    self.cameras[camera_id].release()
                cap = cv2.VideoCapture(device_index)
                if cap.isOpened():
                    self.cameras[camera_id] = cap
                    self.last_pupils[camera_id] = None
                    print(f"Câmera {camera_id} configurada com índice {device_index}")
                else:
                    cap.release()
                    print(f"Falha ao abrir câmera {camera_id} com índice {device_index}")

    def disconnect_all(self):
        with self.pupil_lock:
            for cap in self.cameras.values():
                cap.release()
            self.cameras.clear()
            self.last_pupils.clear()
            print("Todas as câmeras desconectadas")

    def stop(self):
        self.running = False
        self.recording = False
        self.disconnect_all()
        self.out.release()
        print("Gravador de vídeo encerrado")