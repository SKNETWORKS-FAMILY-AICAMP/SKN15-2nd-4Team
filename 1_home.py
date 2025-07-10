import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏠 홈 - 고객 이탈 현황 요약")

# KPI Section
col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 고객 수", "15,200")
col2.metric("이탈 잠재 고객 수", "2,150", "-3.5%")
col3.metric("총 누적 구매 수", "124,000")
col4.metric("오늘의 구매 수", "1,237")

st.divider()

# 이탈 위험 등급 분포
st.subheader("이탈 위험 등급별 고객 분포")
risk_dist = pd.DataFrame({"위험등급": ["High", "Medium", "Low"], "고객수": [500, 1000, 650]})
fig = px.pie(risk_dist, names="위험등급", values="고객수", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# 회원 등급별 이탈율
st.subheader("고객 멤버십별 이탈률 현황")
# 예시 데이터프레임
membership_data = pd.DataFrame({
    "등급": ["Basic", "Silver", "Gold", "Platinum"],
    "이탈률(%)": [30, 20, 10, 5]
})
st.bar_chart(membership_data.set_index("등급"))

# 이탈 Top 고객 표
st.subheader("📉 이탈 가능성 높은 고객 리스트")
# 여기에 예측 데이터에서 top 10만 보여주는 표 삽입
