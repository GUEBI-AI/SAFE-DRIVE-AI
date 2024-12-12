
import time

# 충돌 위험 계산 함수
def calculate_collision_risk(distance, speed):
    """
    충돌 위험을 계산합니다.
    - distance: 객체와의 거리 (m)
    - speed: 속도 (m/s)
    """
    if speed <= 0:
        return "No Immediate Risk"  # 정지 상태
    time_to_collision = distance / speed  # 충돌까지 남은 시간 계산
    if time_to_collision < 2:
        return "Immediate Collision Risk"  # 즉시 충돌 위험
    elif time_to_collision < 5:
        return "Moderate Collision Risk"  # 중간 충돌 위험
    else:
        return "No Immediate Risk"  # 충돌 위험 없음


# 시뮬레이션 데이터
def simulate_data():
    """
    시뮬레이션 데이터를 생성합니다.
    거리(m)와 속도(m/s)를 반환합니다.
    """
    distances = [10, 8, 5, 15, 20]
    speeds = [3, 5, 10, 0, 7]
    for distance, speed in zip(distances, speeds):
        yield distance, speed


# 메인 실행 코드
if __name__ == "__main__":
    print("거리 측정 및 충돌 위험 계산 시스템")
    print("-" * 40)

    for distance, speed in simulate_data():
        print(f"측정된 거리: {distance}m, 속도: {speed}m/s")
        risk = calculate_collision_risk(distance, speed)
        print(f"충돌 위험 수준: {risk}")
        print("-" * 40)
        time.sleep(1)  # 1초 대기
