import pyautogui
import time
import pandas as pd

def inject_tracing_to_vceph(csv_path):
    # 1. 질문자님이 만든 엑셀(CSV) 좌표 읽기
    df = pd.read_csv(csv_path, skiprows=7)
    
    # 2. Vceph 8.6이 켜질 때까지 대기
    print("Vceph 8.6 화면을 클릭하세요. 5초 뒤 시작합니다.")
    time.sleep(5)
    
    # 3. 좌표 하나씩 주입 (광속 클릭)
    for index, row in df.iterrows():
        x, y = row['X'], row['Y']
        
        # 화면 좌표 보정 (Vceph 창 위치에 맞게 조절 필요)
        # pyautogui.moveTo(x, y) 
        pyautogui.click(x, y) 
        
        # 너무 빠르면 Vceph이 못 따라오므로 아주 미세한 지연 시간 추가
        time.sleep(0.01) 

    print("트레이싱 완료! 이제 Vceph에서 저장 버튼을 누르세요.")
