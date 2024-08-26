import time
from PIL import ImageGrab

# 스크린캡쳐를 저장할 디렉토리 지정 (원하는 디렉토리로 변경)
output_file = 'C:/Users/syc720584/OneDrive - samyang.com/바탕 화면/RPA/etc/syc720584_Screen.png'


# 프로그램을 실행하면 무한 루프가 시작됩니다.
while True:
    try:
        screenshot = ImageGrab.grab()  # 스크린캡쳐 수행

        # 스크린캡쳐 덮어쓰기 저장
        screenshot.save(output_file)

        print(f'Screenshot saved as {output_file}')

        # 5초 대기
        time.sleep(5)
    except KeyboardInterrupt:
        # 사용자가 Ctrl+C를 누르면 프로그램 종료
        break