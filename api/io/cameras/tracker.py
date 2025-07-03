import cv2
import numpy as np

class PupilTracker:
    def __init__(self):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def detect_pupil(self, frame):
        try:
            # Reduzir o tamanho da imagem para acelerar o processamento
            scale_factor = 0.5
            small_frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            gray_eq = cv2.equalizeHist(gray)
            blurred = cv2.GaussianBlur(gray_eq, (5, 5), 0)
            _, binary = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY_INV)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, self.kernel)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            largest_area = 0
            largest_ellipse = None

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 200 or area > 15000:
                    continue

                if len(contour) >= 5:
                    ellipse = cv2.fitEllipse(contour)
                    (x, y), (major_axis, minor_axis), angle = ellipse
                    axis_ratio = major_axis / minor_axis
                    if axis_ratio < 0.4 or axis_ratio > 1.6:
                        continue

                    if area > largest_area:
                        largest_area = area
                        largest_ellipse = ellipse

            if largest_ellipse is not None:
                (x, y), (major_axis, minor_axis), angle = largest_ellipse
                x /= scale_factor
                y /= scale_factor
                radius = (major_axis + minor_axis) / 4 / scale_factor
                print(f"Pupila detectada: x={x}, y={y}, r={radius}")
                return [x, y, radius]
            print("Nenhuma pupila detectada")
            return None
        except cv2.error as e:
            print(f"Erro OpenCV na detecção de pupila: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado na detecção de pupila: {e}")
            return None