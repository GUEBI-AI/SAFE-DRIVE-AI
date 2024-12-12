

import cv2
import numpy as np
from transformers import pipeline

# Huggingface 모델 초기화
text_generator = pipeline("text-generation", model="gpt2")

# 비디오 로드
video = cv2.VideoCapture("examples/sample_video.mp4")

# 객체 감지 모델 로드 (예: MobileNet-SSD)
net = cv2.dnn.readNetFromCaffe("models/deploy.prototxt", "models/mobilenet_iter_73000.caffemodel")
classes = ["background", "person", "bicycle", "car", "motorbike", "aeroplane", 
           "bus", "train", "truck", "boat", "traffic light", "fire hydrant"]

while True:
    ret, frame = video.read()
    if not ret:
        break
    
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = classes[idx]
            
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            cv2.putText(frame, text, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Huggingface로 텍스트 생성
            description = text_generator(f"This is a {label}", max_length=20, num_return_sequences=1)
            print(f"Generated description: {description[0]['generated_text']}")

    cv2.imshow("Video Processing", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
