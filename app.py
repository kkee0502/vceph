import streamlit as st
import cv2
import numpy as np
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="Vceph Auto Tracing", layout="wide")

st.title("🦷 Vceph 자동 트레이싱 변환기")
st.write("이미지를 올리면 선을 인식하여 VCE 형식으로 변환합니다.")

# 1. 파일명 입력 및 이미지 업로드
with st.sidebar:
    st.header("설정")
    vce_file_name = st.text_input("생성할 VCE 파일명", value="result_data")
    threshold_val = st.slider("선 인식 감도", 0, 255, 127)

uploaded_file = st.file_uploader("트레이싱 스캔 이미지를 업로드하세요 (JPG, PNG)", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    # 이미지 로드
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 선 인식 (OpenCV)
    # 샤프로 그린 선을 검출하기 위해 이진화 처리
    _, binary = cv2.threshold(gray, threshold_val, 255, cv2.THRESH_BINARY_INV)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="원본 이미지", use_column_width=True)
    with col2:
        st.image(binary, caption="인식된 선 (Preview)", use_column_width=True)

    # 3. 좌표 추출 로직 (단순화된 예시)
    # 실제로는 선의 중심점을 따라가는 알고리즘이 들어갑니다.
    points = np.column_stack(np.where(binary > 0)) # 점들의 위치 추출
    
    st.success(f"총 {len(points)}개의 좌표가 인식되었습니다.")

    # 4. VCE 파일 생성 (바이너리 주입)
    if st.button(f"{vce_file_name}.vce 생성하기"):
        # [핵심] 기존에 주신 11422.vce를 템플릿으로 사용하여 바이너리를 재구성하는 로직
        # 여기서는 설명을 위해 간단한 더미 바이너리를 생성합니다.
        
        # 실제 구현시: 11422.vce의 바이트를 읽어온 뒤, 좌표 구간만 points 데이터로 치환
        dummy_vce_data = b"VCE_HEADER" + points.tobytes() 
        
        st.download_button(
            label="파일 다운로드",
            data=dummy_vce_data,
            file_name=f"{vce_file_name}.vce",
            mime="application/octet-stream"
        )

st.divider()
st.info("Tip: Sella와 Nasion 점이 선명하게 찍혀 있어야 정확한 정합이 가능합니다. -")
