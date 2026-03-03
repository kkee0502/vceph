import streamlit as st
import cv2
import numpy as np
import pandas as pd

st.set_page_config(page_title="Vceph 8.6 Tracing Helper", layout="wide")

st.title("🦷 Vceph 8.6 Tracing Helper (고정밀 인식)")

uploaded_file = st.file_uploader("트레이싱 이미지를 업로드하세요", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    # 1. 이미지 로드 및 그레이스케일 변환
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 노이즈 제거 (선을 부드럽게 유지하면서 잡티만 제거)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. 사이드바 설정 (감도 조절)
    with st.sidebar:
        st.header("인식 설정")
        # 블록 사이즈: 주변 얼마나 넓은 범위를 보고 선인지 판단할지 (홀수여야 함)
        block_size = st.slider("인식 범위 (Block Size)", 3, 51, 21, step=2)
        # 상수 C: 이 값이 클수록 선이 더 가늘게 나오고 노이즈가 줄어듦
        c_val = st.slider("미세 감도 (C value)", 2, 20, 10)

    # 4. 적응형 이진화 (Adaptive Thresholding) - 조명에 상관없이 선을 잘 따옴
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, block_size, c_val
    )

    # 5. 결과 미리보기
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="원본 이미지", use_column_width=True)
    with col2:
        st.image(binary, caption="인식된 선 (이 좌표가 추출됨)", use_column_width=True)

    # 6. 좌표 추출 및 다운로드
    y_coords, x_coords = np.where(binary > 0)
    coords_df = pd.DataFrame({'X': x_coords, 'Y': y_coords})
    
    st.write(f"인식된 점 개수: {len(coords_df)}개")
    
    csv = coords_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="추출된 좌표(CSV) 다운로드",
        data=csv,
        file_name="tracing_points.csv",
        mime="text/csv"
    )
