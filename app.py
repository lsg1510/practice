import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 페이지 설정
st.set_page_config(page_title="성동구 도시건강 데이터 분석", layout="wide")

# 1. 데이터 로드 (보고서 수치 기반 가상 데이터 생성)
@st.cache_data
def load_data():
    # 연도별 핵심 지표 요약 [cite: 98]
    years = [1995, 1998, 2000, 2002, 2004, 2005, 2007, 2010, 2015, 2020, 2024]
    obesity = [29.8, 31.2, 31.9, 32.7, 33.4, 32.8, 30.8, 27.3, 23.7, 21.9, 20.6]
    activity = [28.4, 26.8, 25.8, 24.9, 24.1, 25.1, 28.1, 32.6, 37.2, 38.2, 41.8]
    facilities = [22, 23, 24, 25, 26, 28, 34, 43, 58, 67, 74]
    
    df = pd.DataFrame({
        '연도': years,
        '비만율(%)': obesity,
        '외부활동율(%)': activity,
        '운동시설수': facilities
    })
    return df

df = load_data()

# 사이드바: 연구 개요
st.sidebar.title("연구 개요 [cite: 4]")
st.sidebar.info("""
**연구명**: 서울시 성동구 도시녹지·운동시설과 비만율의 관계 [cite: 1]
**연구 가설**: 외부활동율이 높아질수록 비만율은 낮아질 것이다 [cite: 7, 36]
**주요 이벤트**: 2005년 서울숲 조성 [cite: 28, 52]
""")

# 메인 타이틀
st.title("🌳 성동구 도시건강 리포트 대시보드")
st.markdown("---")

# KPI 섹션
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("2024년 비만율", f"{df.iloc[-1]['비만율(%)']}%", "-12.8%p (vs 2004)") [cite: 53, 77]
with col2:
    st.metric("외부활동율", f"{df.iloc[-1]['외부활동율(%)']}%", "+17.7%p (vs 2004)") [cite: 98]
with col3:
    st.metric("상관계수 (r)", "-0.983", "Strong Negative") [cite: 60, 62]

# 차트 섹션
tab1, tab2, tab3 = st.tabs(["비만율 추세", "상관관계 분석", "연령대별 변화"])

with tab1:
    st.subheader("서울숲 조성 전·후 비만율 변화 [cite: 49]")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x='연도', y='비만율(%)', marker='o', ax=ax, color='teal')
    ax.axvline(x=2005, color='red', linestyle='--', label='서울숲 개장(2005)') [cite: 52]
    ax.legend()
    st.pyplot(fig)
    st.write("2005년 서울숲 개장을 기점으로 비만율 추세가 구조적으로 변화함이 확인되었습니다. [cite: 52, 55]")

with tab2:
    st.subheader("외부활동율 vs 비만율 상관관계 [cite: 57]")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(data=df, x='외부활동율(%)', y='비만율(%)', ax=ax, color='coral')
    st.pyplot(fig)
    st.write("**분석 결과**: 외부활동율이 1%p 증가할 때 비만율이 약 0.68%p 감소합니다. [cite: 61]")

with tab3:
    st.subheader("연령대별 비만율 감소폭 (2004 vs 2024) [cite: 79, 81]")
    age_groups = ['10대', '20대', '30대', '40대', '50대', '60대+']
    reduction = [-51.4, -47.0, -41.0, -38.8, -38.7, -34.6] # 보고서 데이터 [cite: 84, 85, 86]
    
    age_df = pd.DataFrame({'연령대': age_groups, '감소율(%)': reduction})
    st.bar_chart(age_df, x='연령대', y='감소율(%)')
    st.write("10~20대 청년층에서 가장 극적인 개선이 나타났습니다. [cite: 84]")

# 정책 제언 섹션
st.markdown("---")
st.header("📍 정책 제언: 도보 10분의 법칙 [cite: 132, 134]")
st.success("""
- **목표**: 주거지 도보 10분(700m) 이내 운동 시설 접근성 확보 [cite: 135, 136]
- **BCR(비용-편익비)**: 2.8 (초기 투자금 약 5개월 내 회수 가능) [cite: 160]
""")
