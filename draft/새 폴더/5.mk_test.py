# app.py
import streamlit as st
from functions.days_since_prior_order_detail import day_hour_days_since_prior_order  # 파일 import (확장자 없이 이름만)
from functions.days_since_prior_order_detail import user_by_days_since_prior_order  # 파일 import (확장자 없이 이름만)
from functions.days_since_prior_order_detail import user_by_days_since_prior_order_line_graph  # 파일 import (확장자 없이 이름만)
from functions.days_since_prior_order_detail import order_dow_by_days_since_prior_order  # 파일 import (확장자 없이 이름만)
from functions.days_since_prior_order_detail import order_count_by_all_user  # 파일 import (확장자 없이 이름만)

st.title("InstaCart 구매 분석 시각화")



if st.button("요일 + 시간대별 평균 주문 간격 히트맵"):
    fig_1 = day_hour_days_since_prior_order()
    st.pyplot(fig_1)
if st.button("평균 재주문 간격별 사용자 수 (막대그래프)"):
    fig_2 = user_by_days_since_prior_order()
    st.pyplot(fig_2)
if st.button("평균 재주문 간격별 사용자 수 (꺾은선 그래프)"):
    fig_3 = user_by_days_since_prior_order_line_graph()
    st.pyplot(fig_3)
if st.button("요일별 평균 재주문 간격"):
    fig_4 = order_dow_by_days_since_prior_order()
    st.pyplot(fig_4)

if st.button("사용자별 총 주문 횟수 순위"):
    # fig_5 = order_count_by_all_user()
    # st.pyplot(fig_5)
    df = order_count_by_all_user()
    st.dataframe(df) 