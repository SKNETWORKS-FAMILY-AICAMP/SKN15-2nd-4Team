import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

# 등급별로 기준을 다르게 하려고 했으나 민정님이 하고계신거랑 맞춰야 할 것 같아 중단
# 등급부여함수는 괜찮지만 등급별 이탈함수 수정 필요
# 등급부여함수 기준이 달라 이탈도 등급별로 기준 다르게 해야해요
# 등급이 높을 수록 충성도가 있어 기준을 좀 높게 줘도 된다고 잡고 줬던 코드입니당 참고 부탁드려요 !!!

# 와이드 레이아웃 설정
st.set_page_config(layout="wide")

# 1. 데이터 경로 설정
BASE_DIR = Path(__file__).resolve().parent
orders_path = BASE_DIR / "orders.csv"

if not orders_path.exists():
    st.error(f"❌ orders.csv 파일을 찾을 수 없습니다: {orders_path}")
    st.stop()

# 2. 데이터 불러오기
orders = pd.read_csv(orders_path)

# 3. 최근 주문일 계산 (user별 마지막 order 기준)
latest_orders = orders.loc[orders.groupby('user_id')['order_number'].idxmax()]
recent_days = latest_orders.set_index('user_id')['days_since_prior_order'].fillna(999)

# 4. 누적 주문 수 계산
order_count = orders.groupby('user_id')['order_id'].nunique()

# 5. 요약 테이블 생성
summary = pd.DataFrame({
    'recent_days': recent_days,
    'order_count': order_count
}).fillna({'order_count': 0})

# 6. 등급 부여 함수
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

summary['grade'] = summary.apply(assign_grade, axis=1)

# 7. 이탈 판단 함수 (등급별 이탈 기준 다르게 적용)
def is_churned(row):
    days = row['recent_days']
    grade = row['grade']
    
    if grade == 'Platinum' and days > 20:
        return True
    elif grade == 'Gold' and days > 25:
        return True
    elif grade == 'Silver' and days > 15:
        return True
    elif grade == 'Basic' and days > 10:
        return True
    elif grade == 'Inactive':
        return True  # 이미 이탈한 고객
    return False

summary['churned'] = summary.apply(is_churned, axis=1)

# 8. 등급별 이탈율 계산 및 정렬
grade_order = ['Platinum', 'Gold', 'Silver', 'Basic', 'Inactive']
summary['grade'] = pd.Categorical(summary['grade'], categories=grade_order, ordered=True)

grouped = summary.groupby('grade')['churned'].agg(['count', 'sum']).reset_index()
grouped['churn_rate'] = grouped['sum'] / grouped['count'] * 100
grouped = grouped.sort_values('grade')

# 9. Altair 막대그래프 (이탈율)
bar_chart = alt.Chart(grouped).mark_bar(color='tomato').encode(
    x=alt.X('grade', sort=grade_order, title='멤버십 등급'),
    y=alt.Y('churn_rate', title='이탈율 (%)'),
    tooltip=[
        alt.Tooltip('count', title='고객 수'),
        alt.Tooltip('sum', title='이탈 고객 수'),
        alt.Tooltip('churn_rate', title='이탈율 (%)', format='.2f')
    ]
).properties(
    width=700,
    height=400,
    title='멤버십 등급별 이탈율 분포'
)

# 10. 화면 출력
st.title("Instacart 고객 멤버십 등급별 이탈율 분석")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 멤버십 등급별 이탈율")
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.subheader("✅ 멤버십 등급 체계 및 이탈 기준")
    st.markdown("""
| 등급      | 최근 주문일 기준 (days_since_prior_order) | 누적 주문 수 조건 | 이탈 기준 (최근 주문 초과일) | 설명                               |
|-----------|------------------------------------------|------------------|-----------------------------|----------------------------------|
| **Platinum**  | 0 ~ 10일                                 | 5건 이상         | 20일                         | 최근 자주 구매하는 최우수 고객        |
| **Gold**      | 11 ~ 20일                               | 5건 이상         | 25일                         | 충성도 높은 비교적 최근 고객          |
| **Silver**    | 0 ~ 10일                                | 1~4건 이하       | 15일                         | 최근 주문했지만 주문 수 적은 고객     |
| **Basic**     | 0 ~ 29일                                | 0~4건 이하       | 10일                         | 단발성 또는 신규 고객                |
| **Inactive**  | 30일 이상                               | 상관 없음        | 즉시 이탈                    | 장기간 미구매 고객 (이탈 가능성 높음) |
    """)

