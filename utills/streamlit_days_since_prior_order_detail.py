import streamlit as st
from functions.days_since_prior_order_detail import (
    day_hour_days_since_prior_order,
    user_by_days_since_prior_order,
    user_by_days_since_prior_order_line_graph,
    order_dow_by_days_since_prior_order,
    order_count_by_all_user,
)

st.set_page_config(layout="wide")
st.title("🛒 InstaCart 구매 행동 분석 대시보드")
st.markdown("---")
st.sidebar.title("test")
# 📌 1. 요일 + 시간대별 평균 주문 간격
st.subheader("📌 요일 + 시간대별 평균 주문 간격 (히트맵)")
st.markdown("주문 간격의 평균이 요일과 시간에 따라 어떻게 달라지는지 시각화한 히트맵입니다.")
fig1 = day_hour_days_since_prior_order()
st.pyplot(fig1)
st.markdown("---")

# 📌 2. 평균 재주문 간격별 사용자 수 - 막대 + 꺾은선
st.subheader("📌 평균 재주문 간격별 사용자 수")
st.markdown("사용자별 평균 재주문 간격 분포를 시각화한 결과입니다.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**• 막대그래프**")
    fig2 = user_by_days_since_prior_order()
    st.pyplot(fig2)

with col2:
    st.markdown("**• 꺾은선 그래프**")
    fig3 = user_by_days_since_prior_order_line_graph()
    st.pyplot(fig3)

st.markdown("---")

# 📌 3. 요일별 평균 재주문 간격
st.subheader("📌 요일별 평균 재주문 간격")
st.markdown("요일에 따라 재주문 간격이 어떻게 달라지는지 시각화한 막대그래프입니다.")
fig4 = order_dow_by_days_since_prior_order()
st.pyplot(fig4)
st.markdown("---")

# 📌 4. 사용자별 총 주문 횟수 순위
st.subheader("📌 사용자별 총 주문 횟수 순위 (Top 10)")
st.markdown("총 주문 횟수 기준으로 사용자 수가 많은 순으로 정리한 테이블입니다.")
df = order_count_by_all_user()
st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")
st.caption("© 2025 InstaCart 분석 프로젝트 · 팀 SKN15-2nd-4Team")
