import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

# 와이드 레이아웃 설정
st.set_page_config(layout="wide")


# 1. 데이터 로딩 함수
@st.cache_data
def load_data():
    orders_path = "./mydata/orders.csv"

    return pd.read_csv(orders_path)


# 2. 고객별 요약 테이블 생성 함수
def preprocess_data(orders_df: pd.DataFrame) -> pd.DataFrame:
    # 최근 주문일 (user_id별 마지막 order 기준)
    latest_orders = orders_df.loc[orders_df.groupby('user_id')['order_number'].idxmax()]
    recent_days = latest_orders.set_index('user_id')['days_since_prior_order'].fillna(999)

    # 누적 주문 수
    order_count = orders_df.groupby('user_id')['order_id'].nunique()

    # 통합 summary
    summary = pd.DataFrame({
        'recent_days': recent_days,
        'order_count': order_count
    }).fillna({'order_count': 0})

    return summary


# 3. 멤버십 등급 부여 함수
def assign_grade(row):
    days = row['recent_days']
    count = row['order_count']

    if days > 29:
        return 'Inactive'
    if days <= 10:
        if count >= 5:
            return 'Platinum'
        elif count >= 1:
            return 'Silver'
        else:
            return 'Basic'
    if days <= 20:
        if count >= 5:
            return 'Gold'
        else:
            return 'Basic'
    return 'Basic'


# 4. 시각화 함수 (Altair 차트)
def show_membership_chart(summary_df: pd.DataFrame):
    grade_order = ['Platinum', 'Gold', 'Silver', 'Basic', 'Inactive']
    grade_counts = summary_df['grade'].value_counts().reindex(grade_order, fill_value=0).reset_index()
    grade_counts.columns = ['grade', 'count']

    bar_chart = alt.Chart(grade_counts).mark_bar().encode(
        x=alt.X('grade', sort=grade_order, title='등급'),
        y=alt.Y('count', title='고객 수'),
        color=alt.Color('grade', sort=grade_order, legend=None)
    ).properties(
        width=700,
        height=400
    )

    st.subheader("📊 멤버십 등급 분포")
    st.altair_chart(bar_chart, use_container_width=True)


# 5. 등급 설명 표시 함수
def show_grade_description():
    st.subheader("✅ 멤버십 등급 체계 및 설명")
    st.markdown("""
    | 등급      | 최근 주문일 기준 (days_since_prior_order) | 누적 주문 수 조건 | 설명                               |
    |-----------|------------------------------------------|------------------|----------------------------------|
    | **Platinum**  | 0 ~ 10일                                 | 5건 이상         | 최근 자주 구매하는 최우수 고객        |
    | **Gold**      | 11 ~ 20일                               | 5건 이상         | 충성도 높은 비교적 최근 고객          |
    | **Silver**    | 0 ~ 10일                                | 1~4건 이하       | 최근 주문했지만 주문 수 적은 고객     |
    | **Basic**     | 0 ~ 29일                                | 0~4건 이하       | 단발성 또는 신규 고객                |
    | **Inactive**  | 30일 이상                               | 상관 없음        | 장기간 미구매 고객 (이탈 가능성 높음) |
    """)


# 6. 메인 함수
def main():
    st.title("Instacart 고객 멤버십 등급 분석 (최근 주문일 + 누적 주문 수 기준)")

    orders_df = load_data()
    summary_df = preprocess_data(orders_df)
    summary_df['grade'] = summary_df.apply(assign_grade, axis=1)

    show_membership_chart(summary_df)
    show_grade_description()


# # 실행
# if __name__ == "__main__":
#     main()
