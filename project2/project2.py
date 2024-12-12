import cv2
import numpy as np

# YOLO 모델 불러오기 (미리 다운로드된 가중치와 구성 파일 사용)
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# 클래스 이름 로드 (COCO 데이터셋)
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# 영상 파일 열기
video_path = "sample_video.mp4"  # 분석할 영상 파일 경로
cap = cv2.VideoCapture(video_path)

# 위험도 계산 함수
def predict_risk(distance, speed):
    if distance < 10 and speed > 20:
        return "HIGH RISK"
    elif distance < 20:
        return "MODERATE RISK"
    else:
        return "LOW RISK"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width, channels = frame.shape

    # YOLO에 입력을 위한 블롭 생성
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # 탐지된 객체 저장
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # 신뢰도 임계값 설정
            if confidence > 0.5:
                # 객체의 중심과 박스 크기 추출
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # 좌표 계산
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-max suppression으로 중복 제거
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            
            # 거리와 속도 계산 (임의의 값으로 설정)
            distance = 15 - (confidence * 15)  # 거리 추정 (예제)
            speed = np.random.randint(10, 30)  # 속도 추정 (예제)
            
            # 위험도 예측
            risk = predict_risk(distance, speed)
            
            # 객체 감지 결과와 위험도 표시
            color = (0, 0, 255) if risk == "HIGH RISK" else (0, 255, 255) if risk == "MODERATE RISK" else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {risk}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 결과 영상 출력
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
