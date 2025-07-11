# t4_app/check3.py
# ['department', 'product_id', 'user_id', 'order_number', 'days_since_prior_order']

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from utils.data5 import make_data_for_check  # 메모리 최적화 버전 사용



def due_date_churn():
    # ✅ 한글 폰트 설정 (Windows 기준)
    mpl.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    @st.cache_data
    def load_data():
        return make_data_for_check()

    st.title("🧓 유효기간 짧은 상품과 고객 이탈 관계 분석")

    data = load_data()

    # 유효기간 짧은 소분류 기준 정의
    short_shelf_life_departments = ['produce', 'dairy eggs', 'fresh fruits', 'fresh vegetables']
    short_shelf_products = data[data['department'].isin(short_shelf_life_departments)]

    # 주문 데이터 분리
    short_shelf_order = data[data['product_id'].isin(short_shelf_products['product_id'])]
    other_order = data[~data['product_id'].isin(short_shelf_products['product_id'])]

    # ✅ 평균 구매 간격 계산 함수
    def get_avg_purchase_interval(df):
        df = df[['user_id', 'order_number', 'days_since_prior_order']].drop_duplicates()
        df['days_since_prior_order'] = df['days_since_prior_order'].fillna(0)
        avg_interval = (
            df.groupby('user_id')['days_since_prior_order']
            .mean()
            .reset_index()
            .rename(columns={'days_since_prior_order': 'avg_days_between_orders'})
        )
        return avg_interval

    short_interval = get_avg_purchase_interval(short_shelf_order)
    other_interval = get_avg_purchase_interval(other_order)

    # ✅ 고객별 이탈 여부 계산
    data_sorted = data[['user_id', 'order_number', 'days_since_prior_order']].drop_duplicates()
    data_sorted = data_sorted.sort_values(['user_id', 'order_number'])
    data_sorted['days_since_prior_order'] = data_sorted['days_since_prior_order'].fillna(0)
    data_sorted['cum_days'] = data_sorted.groupby('user_id')['days_since_prior_order'].cumsum()

    last_order = data_sorted.groupby('user_id')['cum_days'].max().reset_index()
    max_day = data_sorted['cum_days'].max()
    last_order['churn'] = last_order['cum_days'].apply(lambda x: 1 if max_day - x > 30 else 0)

    # ✅ 분석 테이블 병합
    analysis = (
        last_order
        .merge(short_interval, on='user_id', how='left')
        .merge(other_interval, on='user_id', how='left', suffixes=('_short', '_other'))
    )
    analysis = analysis.dropna()

    st.subheader("📉 유효기간 짧은 상품의 구매 가능과 고객 이탈 관계")

    # ✅ 이탈 여부별 요약 통계
    summary = (
        analysis
        .groupby('churn')['avg_days_between_orders_short']
        .agg(['mean', 'std'])
        .reset_index()
    )
    summary['churn'] = summary['churn'].map({0: '이탈 아님', 1: '이탈'})

    # ✅ 박스플롯 + 평균 점 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=analysis['churn'].map({0: '이탈 아님', 1: '이탈'}),
                y=analysis['avg_days_between_orders_short'],
                palette='Set2',
                showfliers=False,
                ax=ax)

    for i, row in summary.iterrows():
        ax.scatter(i, row['mean'], color='red', s=100, label='평균' if i == 0 else "")

    ax.set_title('유효기간 짧은 상품 구매 주기별 고객 이탈 비교', fontsize=16)
    ax.set_xlabel('고객 이탈 여부', fontsize=14)
    ax.set_ylabel('평균 구매 간격 (일)', fontsize=14)
    ax.legend()

    st.pyplot(fig)

    st.caption("※ 기준: 마지막 구매 이후 30일 이상 주문이 없으면 '이탈'로 간주")

    # ✅ 그래프 아래 설명
    with st.expander("🔹 구독 가정을 목적으로 한 분석 설명 보기"):
        st.markdown("""
        - 특정 상품을 얼마나 자주 구매하는지에 따라 고객이 이탈하는 경향이 있는지를 파악하려는 목.
        - 빨간 점(평균)을 통해 **이탈 그룹**과 **비이탈 그룹** 간의 **평균 간격 차이**가 뚜렷하게 나타남.

        ### 💡 결론 및 인사이트
        - 유효기간이 짧은 상품의 경우, 평균 구매 간격이 길어지는 고객은 **이탈 가능성이 높다**는 중요한 패턴 도출 가능.
        - 이를 기반으로:
            - **장기간 구매 이력이 없는 고객**을 **이탈 위험군**으로 사전 탐지하고
            - **리마인드 메시지**나 **할인 쿠폰** 등 **재구매 유도 마케팅**을 적용가능.
        """)

# # 실행
# if __name__ == '__main__':
#     total()
