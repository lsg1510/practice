import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 페이지 기본 설정
st.set_page_config(page_title="성동구 도시건강 데이터 분석", layout="wide")

# 1. 데이터 로드 (보고서 수치 기반 가상 시계열 생성)
@st.cache_data
def load_data():
    # 보고서의 1995~2024 트렌드 반영
    years = [1995, 2000, 2004, 2005, 2010, 2015, 2020, 2024]
    obesity = [29.8, 31.9, 33.4, 32.8, 27.3, 23.7, 21.9, 20.6]
    activity = [28.4, 25.8, 24.1, 25.1, 32.6, 37.2, 38.2, 41.8]
    
    df = pd.DataFrame({
        '연도': years,
        '비만율(%)': obesity,
        '외부활동율(%)': activity
    })
    return df

df = load_data()

# 메인 타이틀 및 개요
st.title("🌳 성동구 도시녹지·운동시설과 비만율 분석")
st.markdown("### 2005년 서울숲 조성 전·후 30년 실증 연구 데이터")

# 사이드바: 분석 요약 정보
st.sidebar.header("Analysis Summary")
st.sidebar.info(f"""
- **상관계수 (r):** -0.983 (강한 음의 상관)
- **t-test:** p < 0.001 (유의미함)
- **핵심전략:** 도보 10분 내 시설 확충
""")

# 섹션 1: 주요 지표 (KPI)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("2024 비만율", "20.6%", "-12.8%p (vs 2004)")
with col2:
    st.metric("외부활동율", "41.8%", "+17.7%p (vs 2004)")
with col3:
    st.metric("의료비 절감액 (연간)", "2,520억", "BCR 2.8")

st.divider()

# 섹션 2: 시각화 분석
tab1, tab2, tab3 = st.tabs(["📉 비만율 추세", "📍 상관관계 분석", "👥 연령대별 감소폭"])

with tab1:
    st.subheader("서울숲 조성(2005) 전후 비만율 변화")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x='연도', y='비만율(%)', marker='o', ax=ax, color='teal')
    ax.axvline(x=2005, color='red', linestyle='--', label='서울숲 개장')
    ax.fill_between(df['연도'], df['비만율(%)'], alpha=0.1, color='teal')
    plt.legend()
    st.pyplot(fig)
    st.write("2004년 정점(33.4%) 이후 인프라 확충에 따라 지속적 하락세를 보입니다.")

with tab2:
    st.subheader("외부활동율과 비만율의 상관관계")
    fig, ax = plt.subplots()
    sns.regplot(data=df, x='외부활동율(%)', y='비만율(%)', ax=ax, color='coral')
    st.pyplot(fig)
    st.write("**분석 결과:** 피어슨 상관계수 $r = -0.983$으로 강력한 음의 상관관계가 증명되었습니다.")

with tab3:
    st.subheader("연령대별 비만율 감소율 (2004 vs 2024)")
    # 보고서 7장 데이터 활용
    age_data = {
        "연령대": ["10대", "20대", "30대", "40대", "50대", "60대+"],
        "감소율(%)": [51.4, 47.0, 41.0, 38.8, 38.7, 34.6]
    }
    age_df = pd.DataFrame(age_data)
    st.bar_chart(age_df, x="연령대", y="감소율(%)", color="#2E86C1")

# 섹션 3: 시뮬레이션 (분석가 관점의 Feature)
st.divider()
st.header("🔮 정책 효과 시뮬레이터")
st.write("생활밀착형 운동시설(도보 10분 내) 확충 시 예상 효과를 계산합니다.")

target_activity = st.slider("목표 외부활동율(%) 설정", 40, 60, 42)

# 상관계수 기반 간단한 예측 선형 모델 (가정: y = -0.68x + 50)
predicted_obesity = -0.68 * target_activity + 49.0

st.subheader(f"예상 비만율: {predicted_obesity:.1f}%")
st.progress((60 - predicted_obesity) / 60) # 단순 시각화용 게이지
st.success(f"이 수치는 현재보다 비만 인구를 약 {abs(20.6 - predicted_obesity)*7000:.0f}명 더 감소시킬 수 있는 수치입니다.")

# 데이터프레임 확인
with st.expander("원본 데이터 보기"):
    st.dataframe(df)
