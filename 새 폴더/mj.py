# mj.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (예: 나눔고딕이 설치되어 있을 경우)
plt.rcParams['font.family'] = 'NanumGothic'  # 또는 'Malgun Gothic', 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지



def render_dashboard():
    # --- 데이터 불러오기 ---
    @st.cache_data
    def load_data():
        df = pd.read_csv('./pages/functions/user_pattern.csv')
        return df

    df = load_data()
    user_pattern = load_data()

    # --- 1단계: 평균 구매 주기 분석 ---
    st.subheader("1. 평균 구매 주기 분석 → 루틴과 이탈 경향 파악")

    st.markdown("""
    - **의미**: 고객이 플랫폼에 얼마나 자주 방문하고 있는지 보여주는 지표
    - **인사이트**:
        - 평균 주기가 **20일 이상인 고객**은 이탈 위험이 상대적으로 높음
        - 평균 주기가 짧은 고객은 **루틴하게 사용하는 충성 고객 가능성**
    """)

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.histplot(user_pattern['avg_order_interval'], bins=30, kde=True, color='skyblue', ax=ax1)
    plt.axvline(x=20, color='red', linestyle='--', label='이탈 경계선 예시')
    plt.title('고객 평균 주문 주기 분포')
    plt.xlabel('평균 주문 주기 (일)')
    plt.ylabel('고객 수')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig1)

    # --- 2단계: 평균 주문 수 분석 ---
    st.subheader("2. 평균 주문 수 분석 → 충성도, LTV 추정")

    st.markdown("""
    - **의미**: 고객이 플랫폼에서 얼마나 자주, 많이 주문했는지를 보여주는 지표
    - **인사이트**:
        - 평균보다 많이 주문한 고객은 충성도가 높고 VIP로 볼 수 있음
        - 주문 수가 적은 고객은 신규/이탈 위험 가능성
    """)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(user_pattern['total_orders'], bins=30, color='mediumseagreen', ax=ax2)
    plt.axvline(user_pattern['total_orders'].mean(), color='red', linestyle='--', label=f"평균 주문 수: {user_pattern['total_orders'].mean():.2f}")
    plt.yscale('log')
    plt.title('고객 총 주문 수 분포 (Log Scale)')
    plt.xlabel('총 주문 수')
    plt.ylabel('고객 수 (로그)')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig2)

    # --- 3단계: 재주문 비율 분석 ---
    st.subheader("3. 전체 재주문 비율 분석 → 반복구매 성향, 제품 만족도")

    st.markdown("""
    - **의미**: 고객이 같은 제품을 반복 구매하는 경향성 (충성도 높은 고객 확인 가능)
    - **인사이트**:
        - 재주문 비율이 0.7 이상이면 제품/플랫폼에 대한 만족도가 높음
        - 0.4 이하면 충성도 낮음 또는 일회성 이용 가능성
    """)

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.kdeplot(user_pattern['reorder_ratio'], fill=True, color='orange', ax=ax3)
    plt.axvline(user_pattern['reorder_ratio'].mean(), color='red', linestyle='--', label='전체 평균')
    plt.title('고객 재주문 비율 분포')
    plt.xlabel('재주문 비율')
    plt.ylabel('밀도')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig3)

    # --- 4. 주문 수 vs 재주문 비율 산점도 ---
    st.subheader("4. 고객 유형 관계 시각화")

    fig4, ax4 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=user_pattern, x='total_orders', y='reorder_ratio', alpha=0.5, ax=ax4)
    plt.axvline(20, color='red', linestyle='--', label='충성 고객 기준 (20회 이상)')
    plt.axhline(0.7, color='orange', linestyle='--', label='재주문율 기준 (70% 이상)')
    plt.title('총 주문 수 vs 재주문 비율')
    plt.xlabel('총 주문 수')
    plt.ylabel('재주문 비율')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig4)


    # --- 5. 고객 충성도 및 행동 세그먼트 비교 시각화 ---
    # --- 데이터 불러오기 ---
    @st.cache_data
    def load_data():
        df = pd.read_csv(r'C:\Users\user\Downloads\t4_app_v2\pages\functions\user_pattern.csv')
        return df

    df = load_data()

    # --- 주요 지표 계산 (user_pattern 생성) ---
    st.subheader("5. 고객 충성도 세그먼트 분포 비교")

    # 1) 충성도 기반 세그먼트

    def classify_customer(row):
        if row['total_orders'] >= 20 and row['reorder_ratio'] >= 0.7:
            return 'VIP 충성 고객'
        elif row['total_orders'] >= 10 and row['reorder_ratio'] >= 0.5:
            return '일반 충성 고객'
        elif row['total_orders'] < 10 and row['reorder_ratio'] < 0.4:
            return '이탈 위험군'
        else:
            return '기타'

    user_pattern['loyalty_segment'] = user_pattern.apply(classify_customer, axis=1)

    # 2) 행동 기반 세그먼트

    def segment_customer(row):
        if row['total_orders'] >= 10 and row['reorder_ratio'] > 0.7:
            return '충성 고객'
        elif row['avg_order_interval'] > 20:
            return '이탈 위험'
        elif row['total_orders'] <= 3:
            return '신규/저활성 고객'
        else:
            return '일반 고객'

    user_pattern['behavior_segment'] = user_pattern.apply(segment_customer, axis=1)

    # 바 차트로 비교 시각화
    fig, ax = plt.subplots(figsize=(10, 5))
    user_pattern['loyalty_segment'].value_counts().sort_index().plot(
        kind='bar', color='tomato', width=0.4, label='충성도 기준', position=1, ax=ax)
    user_pattern['behavior_segment'].value_counts().sort_index().plot(
        kind='bar', color='skyblue', width=0.4, label='행동 기준', position=0, ax=ax)

    plt.title('충성도 vs 행동 기반 고객 세그먼트 분포')
    plt.ylabel('고객 수')
    plt.xticks(rotation=0)
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

    # 분석 설명 표시
    st.markdown("""
    🔍 **분석 인사이트**
    - 충성도 기준 분류는 주문 횟수 + 재주문 비율 기반 → VIP 식별에 적합
    - 행동 기준 분류는 구매 주기까지 반영 → 이탈 조기 감지 가능
    - 두 기준이 완전히 일치하지 않음 → 다양한 관점의 고객 대응 필요
    """)

    # --- 6. 클러스터 기반 고객 행동 유형 분석 ---
    import numpy as np

    st.subheader("6. 고객 행동 유형 클러스터 분석 (KMeans 기반)")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=user_pattern,
        x='avg_order_interval',
        y='reorder_ratio',
        hue='cluster',
        palette='Set2',
        alpha=0.7,
        size='total_orders',
        sizes=(20, 200),
        ax=ax
    )

    # y축 범위 및 촘촘한 간격 설정
    ax.set_ylim(0.7, 1.0)
    ax.set_yticks(np.arange(0.7, 1.01, 0.01))  # 0.01 간격으로 촘촘하게 표시

    # 기준선 추가 (얇게)
    plt.axvline(x=20, color='gray', linestyle='--', linewidth=0.7)
    plt.axhline(y=0.5, color='gray', linestyle='--', linewidth=0.7)

    # 라벨 및 제목
    plt.title('고객 행동 유형 클러스터 (KMeans)', fontsize=14)
    plt.xlabel('평균 주문 주기 (일)')
    plt.ylabel('재주문 비율')
    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.legend(title='클러스터', bbox_to_anchor=(1.05, 1))

    st.pyplot(fig)

    st.markdown("""
    🔍 **클러스터 해석 요약**
    | 클러스터 | 평균 주문 주기 | 주문 수 | 재주문율 | 해석 |
    |----------|----------------|--------|----------|----------------|
    | 0 | 8.5일 | 13.4 | 0.82 | 핵심 충성 고객 |
    | 1 | 23.1일 | 4.2 | 0.33 | 이탈 위험 고객 |
    | 2 | 11.2일 | 3.1 | 0.25 | 신규/저활성 고객 |
    | 3 | 15.0일 | 6.5 | 0.70 | 일반 유지 고객 |
    """)

    # --- 7. 충성도 등급별 평균 지표 히트맵 ---
    st.subheader("7. 충성도 등급별 평균 지표 히트맵")

    def classify_loyalty(row):
        if row['total_orders'] >= 30 and row['reorder_ratio'] >= 0.7:
            return 'VIP'
        elif row['total_orders'] >= 15 and row['reorder_ratio'] >= 0.5:
            return '충성 고객'
        elif row['total_orders'] < 10 and row['reorder_ratio'] < 0.4:
            return '신규 고객'
        else:
            return '일반 고객'

    user_pattern['loyalty_level'] = user_pattern.apply(classify_loyalty, axis=1)

    # 히트맵용 데이터
    loyalty_summary = user_pattern.pivot_table(
        index='loyalty_level',
        values=['avg_order_interval', 'total_orders', 'reorder_ratio'],
        aggfunc='mean'
    ).round(2)

    # 한글 컬럼명
    loyalty_summary = loyalty_summary.rename(columns={
        'avg_order_interval': '평균 구매 주기(일)',
        'total_orders': '총 주문 수',
        'reorder_ratio': '재주문 비율'
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(loyalty_summary, annot=True, cmap='YlGnBu', fmt=".2f", ax=ax)
    plt.title('충성도 등급별 평균 지표 히트맵')
    plt.ylabel('고객 등급')
    plt.xlabel('지표')
    st.pyplot(fig)

    st.markdown("""
    ✅ **분석 요약**
    - VIP 고객은 평균 30회 이상 주문하며 재구매 비율도 매우 높음 → 핵심 유치 대상
    - 신규 고객은 주기 길고 재주문 거의 없음 → 이탈 전환 가능성
    - 일반 고객군은 활동성 중간 → 마케팅 캠페인 대상
    """)
