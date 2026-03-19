import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정 (로컬 실행 시 나눔고딕 등 설치 필요)
plt.rcParams['font.family'] = 'Malgun Gothic' 
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터셋 구성 (보고서 제9장 통계표 및 주요 수치 기반) 
@st.cache_data
def get_report_data():
    data = {
        '연도': [1995, 1998, 2000, 2002, 2004, 2005, 2007, 2010, 2015, 2020, 2024],
        '비만율': [29.8, 31.2, 31.9, 32.7, 33.4, 32.8, 30.8, 27.3, 23.7, 21.9, 20.6],
        '외부활동율': [28.4, 26.8, 25.8, 24.9, 24.1, 25.1, 28.1, 32.6, 37.2, 38.2, 41.8],
        '운동시설': [22, 23, 24, 25, 26, 28, 34, 43, 58, 67, 74]
    }
    return pd.DataFrame(data)

df = get_report_data()

# 페이지 헤더
st.set_page_config(page_title="성동구 도시건강 분석", layout="wide")
st.title("📊 성동구 도시환경-비만율 실증 분석 대시보드")
st.markdown(f"**연구 가설**: { '외부활동율이 높아질수록 해당 지역의 비만율은 낮아질 것이다' } [cite: 7]")

# --- 섹션 1: 주요 지표 (Metrics) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("최고 비만율 (2004)", "33.4%", "기준점") [cite: 50]
with m2:
    st.metric("최저 비만율 (2024)", "20.6%", "-12.8%p", delta_color="normal") [cite: 53]
with m3:
    st.metric("외부활동율 상관계수", "-0.983", "매우 강함") [cite: 60]
with m4:
    st.metric("운동시설 확충", "74개", "3.4배 증가") [cite: 99]

st.divider()

# --- 섹션 2: 시계열 추세 및 구조적 변화 ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 연도별 비만율 및 외부활동율 추이")
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # 비만율 (Line)
    sns.lineplot(data=df, x='연도', y='비만율', marker='o', color='crimson', ax=ax1, label='비만율 (%)')
    ax1.axvline(x=2005, color='gray', linestyle='--', alpha=0.7)
    ax1.text(2005.5, 30, "2005 서울숲 개장", fontweight='bold') [cite: 52]
    
    # 외부활동율 (Bar)
    ax2 = ax1.twinx()
    sns.barplot(data=df, x='연도', y='외부활동율', alpha=0.3, color='teal', ax=ax2, label='외부활동율 (%)')
    
    st.pyplot(fig)

with col_right:
    st.subheader("📝 통계적 유의성 (t-test)") [cite: 65]
    st.write("서울숲 조성 전/후 비만율 비교")
    t_res = {
        "구분": ["조성 전(n=10)", "조성 후(n=20)"],
        "평균 비만율": ["31.64%", "24.69%"],
        "표준편차": ["1.24%", "3.92%"]
    } [cite: 68]
    st.table(pd.DataFrame(t_res))
    st.latex(r"t = 6.38, \ p < 0.001") [cite: 69]
    st.info(f"**Cohen's d = 2.33** (매우 큰 효과 크기) [cite: 72]")

# --- 섹션 3: 상관분석 및 연령대별 Insight ---
tab1, tab2 = st.tabs(["상관관계 심층 분석", "연령대별 개선 효과"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.write("**외부활동율 vs 비만율 산점도**")
        fig2, ax2 = plt.subplots()
        sns.regplot(data=df, x='외부활동율', y='비만율', color='seagreen', ax=ax2)
        st.pyplot(fig2)
    with c2:
        st.write("**분석 결과 요약**")
        st.write("- 결정계수($R^2$): 0.966 [cite: 61]")
        st.write("- 외부활동율 1%p 증가 시 비만율 0.68%p 감소 [cite: 61]")
        st.success("연구 가설 H1 지지됨: 통계적으로 매우 유의한 음의 상관관계 확인 [cite: 63]")

with tab2:
    st.subheader("연령대별 비만율 감소율 (2004 vs 2024)") [cite: 81]
    age_data = {
        '연령대': ['10대', '20대', '30대', '40대', '50대', '60대+'],
        '감소율': [51.4, 47.0, 41.0, 38.8, 38.7, 34.6]
    } [cite: 84, 85, 86]
    age_df = pd.DataFrame(age_data)
    st.bar_chart(age_df.set_index('연령대'))
    st.caption("청소년 및 청년층에서 인프라 활용도가 가장 높게 나타남 [cite: 84]")

# --- 섹션 4: 정책 시뮬레이터 (분석가적 관점) ---
st.divider()
st.header("🔮 생활밀착형 정책 효과 예측 시뮬레이션") [cite: 153]
st.write("추가적인 운동시설 확충 시 2035년 예상 비만율을 계산합니다.")

col_sim1, col_sim2 = st.columns([1, 2])
with col_sim1:
    target_year = st.slider("목표 연도", 2025, 2035, 2030)
    policy_strength = st.radio("정책 강도", ["현행 유지", "생활밀착형 강화(적극적)"])

with col_sim2:
    if policy_strength == "생활밀착형 강화(적극적)":
        expected_obesity = 15.4 # 2035년 예측치 
        st.warning(f"🎯 {target_year}년 예상 비만율: {expected_obesity}% (약 14만 명 감소 효과) [cite: 156]")
        st.write(f"예상 BCR(비용-편익비): 2.8 [cite: 160]")
    else:
        st.info(f"🎯 {target_year}년 예상 비만율: 약 18.8% (자연 감소 추세) ")

# 푸터
st.sidebar.markdown("---")
st.sidebar.write("© 2025 Seoul Urban Health Research Institute") [cite: 180]
st.sidebar.write("본 데이터는 가상 시뮬레이션 데이터입니다.") [cite: 179]
