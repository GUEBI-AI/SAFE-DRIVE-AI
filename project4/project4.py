
---

### **Python 코드**
```python
def adjust_sensitivity(lighting_level, weather_condition):
    """
    민감도를 조정합니다.
    - lighting_level: 조명 강도(Lux)
    - weather_condition: 날씨 조건 ("Rain", "Snow", "Clear" 등)
    """
    if lighting_level < 50 or weather_condition in ["Rain", "Snow"]:
        return "Increase Sensitivity"  # 민감도 증가
    else:
        return "Normal Sensitivity"   # 정상 민감도


# 시뮬레이션 데이터 생성
def simulate_environment():
    """
    조명 수준(Lux)과 날씨 조건을 시뮬레이션합니다.
    """
    simulated_data = [
        {"lighting_level": 40, "weather_condition": "Rain"},   # 비가 오고 조도가 낮음
        {"lighting_level": 70, "weather_condition": "Clear"},  # 맑고 조도가 높음
        {"lighting_level": 30, "weather_condition": "Snow"},   # 눈이 오고 조도가 낮음
        {"lighting_level": 90, "weather_condition": "Cloudy"}, # 흐림
    ]
    for data in simulated_data:
        yield data


# 메인 실행 코드
if __name__ == "__main__":
    print("날씨/조명 조건 대응 시스템")
    print("-" * 40)

    # 시뮬레이션 데이터 실행
    for environment in simulate_environment():
        lighting_level = environment["lighting_level"]
        weather_condition = environment["weather_condition"]

        print(f"조명 강도: {lighting_level} Lux, 날씨 상태: {weather_condition}")
        sensitivity = adjust_sensitivity(lighting_level, weather_condition)
        print(f"시스템 민감도: {sensitivity}")
        print("-" * 40)
