import streamlit as st
import cv2
import numpy as np
import pandas as pd

st.title("🦷 Vceph 8.6 Tracing Helper")

# 1. 파일 업로드
uploaded_file = st.file_uploader("스캔 이미지를 올려주세요", type=['jpg', 'png'])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # [인식 로직] 샤프 선 추출 (OpenCV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # 좌표 추출
    y_coords, x_coords = np.where(binary > 0)
    coords_df = pd.DataFrame({'X': x_coords, 'Y': y_coords})

    st.image(binary, caption="인식된 선 미리보기", width=500)
    
    # 2. 결과물을 CSV로 내보내기
    # Vceph 8.6에 직접 주입할 데이터입니다.
    csv = coords_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="추출된 좌표(CSV) 다운로드",
        data=csv,
        file_name="tracing_points.csv",
        mime="text/csv"
    )
