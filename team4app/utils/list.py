
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# 와이드 레이아웃 설정
st.set_page_config(layout="wide")

# ✅ 1. 고객이탈리스트.csv 경로 설정
csv_path = Path("/home/min/workspace/Project_2/mydata/고객이탈리스트.csv")

if not csv_path.exists():
    st.error(f"❌ 고객이탈리스트.csv 파일을 찾을 수 없습니다: {csv_path}")
    st.stop()

# ✅ 2. 데이터 불러오기
df = pd.read_csv(csv_path)

# ✅ 3. 등급 부여 함수 (마지막주문일 + 총주문수 기준)
def assign_grade(row):
    days = row['마지막주문일']
    orders = row['총주문수']

    if days > 30:
        return 'Inactive'
    elif days <= 10 and orders >= 10:
        return 'Platinum'
    elif days <= 20 and orders >= 5:
        return 'Gold'
    elif days <= 10 and orders >= 3:
        return 'Silver'
    else:
        return 'Basic'

df['등급'] = df.apply(assign_grade, axis=1)

# ✅ 4. 이탈여부는 csv 기준 사용
df['이탈여부'] = df['이탈가능성여부'].astype(bool)

# ✅ 5. 등급 정렬 기준 지정
grade_order = ['Platinum', 'Gold', 'Silver', 'Basic', 'Inactive']
df['등급'] = pd.Categorical(df['등급'], categories=grade_order, ordered=True)

# ✅ 6. 등급별 이탈율 계산
grouped = df.groupby('등급')['이탈여부'].agg(['count', 'sum']).reset_index()
grouped['이탈율'] = (grouped['sum'] / grouped['count']) * 100
grouped = grouped.sort_values('등급')

# ✅ 7. Altair 막대그래프 시각화
bar_chart = alt.Chart(grouped).mark_bar(color='tomato').encode(
    x=alt.X('등급', sort=grade_order, title='멤버십 등급'),
    y=alt.Y('이탈율', title='이탈율 (%)'),
    tooltip=[
        alt.Tooltip('count', title='고객 수'),
        alt.Tooltip('sum', title='이탈 고객 수'),
        alt.Tooltip('이탈율', title='이탈율 (%)', format='.2f')
    ]
).properties(
    width=700,
    height=400,
    title='멤버십 등급별 이탈율 분포 (고객이탈리스트.csv 기준)'
)

# ✅ 8. Streamlit 화면 출력
st.title("고객 멤버십 등급별 이탈율 분석 (CSV 기반)")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 멤버십 등급별 이탈율")
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.subheader("✅ 멤버십 등급 기준 및 이탈 기준 설명")
    st.markdown("""
| 등급        | 최근 주문일 기준 (마지막주문일) | 누적 주문 수 조건 | 이탈 기준 (30일 초과) | 설명                               |
|-------------|------------------------------|------------------|---------------------|----------------------------------|
| **Platinum**  | 0 ~ 10일                        | 10건 이상         | X                   | 최근 자주 구매하는 최우수 고객        |
| **Gold**      | 11 ~ 20일                      | 5건 이상          | X                   | 충성도 높은 비교적 최근 고객          |
| **Silver**    | 0 ~ 10일                        | 3~4건             | X                   | 최근 주문했지만 주문 수 적은 고객     |
| **Basic**     | ~ 29일 이하                     | 그 외             | X                   | 단발성 또는 신규 고객                |
| **Inactive**  | 30일 초과                       | 무관              | ✅                  | 장기 미구매 고객 (이탈로 간주됨)      |
    """)
