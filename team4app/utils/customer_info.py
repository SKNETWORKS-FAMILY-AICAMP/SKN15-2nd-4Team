import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def customer_info():
    data=pd.read_csv('./mydata/tmp5.csv')
    customer_number = data.user_id.nunique()
    buying_number = data['max_items'].sum()
    order_number = data.order_id.nunique()

    # KPI Section
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전체 고객 수", f"{customer_number:,}")
    col2.metric("이탈 잠재 고객 수", "41,547")
    col3.metric("누적 주문 수", f"{order_number:,}")
    col4.metric("누적 판매 상품 수", f"{buying_number:,}")

    st.divider()

    # 이탈 위험 등급 분포
    st.subheader("이탈 위험 등급별 고객 분포")
    st.image("../images/Types of risk groups for leaving.png", caption="이탈 위험군 타입별 비율(%)", use_container_width=True)
    st.image("../images/dropout_risk_groups.png",caption="전체 고객의 이탈 위험군 vs 비위험군 비율(%)", use_container_width=True)

