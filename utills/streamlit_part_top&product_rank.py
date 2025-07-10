import streamlit as st
from functions.Products_Rank import (
    Products_Rank,
    Products_Under_Rank,
    )
from functions.Part_Top_rank import Product_Count_Per_Department

st.set_page_config(layout="wide")
st.title("🛍️ InstaCart 제품 통계 시각화")
st.markdown("고객 선호도 및 부서별 제품 정보를 시각화한 결과입니다.")
st.markdown("---")

# 🎯 상단 2개 그래프: 좌우 분할
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔺 Top 10 Products by Percent")
    fig1 = Products_Rank()
    st.pyplot(fig1)

with col2:
    st.subheader("📦 Products per Department")
    fig2 = Product_Count_Per_Department()
    st.pyplot(fig2)

st.markdown("---")
st.subheader("🌟 Top 20 Most Ordered Products")
fig3 = Products_Under_Rank()
st.pyplot(fig3)