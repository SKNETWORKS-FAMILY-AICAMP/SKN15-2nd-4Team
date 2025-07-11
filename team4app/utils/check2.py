import streamlit as st
import pandas as pd
import matplotlib as mpl
from utils.data5 import make_data5  # 메모리 최적화된 전처리 함수

# # 전체 페이지 레이아웃
# st.set_page_config(layout="wide")

# # 한글 폰트 설정 (윈도우 기준)
# mpl.rc('font', family='Malgun Gothic')
# st.markdown("""
# <style>
# thead tr th:first-child {display:none}
# tbody th {display:none}
# </style>
# """, unsafe_allow_html=True)


@st.cache_data
def load_data():
    return make_data5()

def highlight_rank(s):
    color = '#cfe2f3'  # 연한 하늘색 강조
    return [f'background-color: {color}' if col == '순위' else '' for col in s.index]

def reorder_rate_ranking():
    #st.title("📋 상품 재구매율 랭킹")
    st.markdown("""
    이 페이지는 고객들이 얼마나 자주 같은 상품을 재구매하는지를 기반으로  
    **Top 10 / Bottom 10 재구매율 상품**을 나란히 제공합니다.
    """)

    data = load_data()

    # 1. 재구매율 계산
    reorder_rate = (
        data.groupby('product_name')['reordered']
        .mean()
        .reset_index()
        .rename(columns={'reordered': '재구매율'})
    )

    # 2. 주문 수 계산
    order_count = data['product_name'].value_counts().reset_index()
    order_count.columns = ['product_name', '주문수']

    # 3. 병합 및 필터링 (50회 이상)
    reorder_rate = reorder_rate.merge(order_count, on='product_name')
    reorder_rate_filtered = reorder_rate[reorder_rate['주문수'] >= 50]

    # 4. 상위/하위 랭킹
    top_10 = reorder_rate_filtered.sort_values('재구매율', ascending=False).head(10).reset_index(drop=True)
    bottom_10 = reorder_rate_filtered.sort_values('재구매율', ascending=True).head(10).reset_index(drop=True)

    top_10.insert(0, '순위', top_10.index + 1)
    bottom_10.insert(0, '순위', bottom_10.index + 1)

    # 5. 컬럼 레이아웃
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ 재구매율 Top 10")
        styled_top = top_10[['순위', 'product_name', '재구매율', '주문수']] \
            .rename(columns={'product_name': '상품명'}) \
            .style.format({'재구매율': '{:.1%}'}) \
            .apply(highlight_rank, axis=1)
        st.dataframe(styled_top, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🔻 재구매율 Bottom 10")
        styled_bottom = bottom_10[['순위', 'product_name', '재구매율', '주문수']] \
            .rename(columns={'product_name': '상품명'}) \
            .style.format({'재구매율': '{:.1%}'}) \
            .apply(highlight_rank, axis=1)
        st.dataframe(styled_bottom, use_container_width=True, hide_index=True)

    # 6. 설명 추가
    with st.expander("ℹ️ 재구매율과 주문수 관계 설명 보기", expanded=True):
        st.markdown("""
        ### 🎯 질문:
        > 재구매율 상위 상품과 하위 상품의 '주문 수'가 비슷한데, 왜 이런 현상이 발생하나요?

        ### ✅ 답변:
        - **주문 수는 '인기도', 재구매율은 '충성도'**를 나타냅니다.
        - Top 10 / Bottom 10 모두 일정 수준 이상 자주 팔리는 상품들입니다 (50회 이상).
        - 하지만 **누가, 몇 번 반복해서 사느냐가 다릅니다.**
        - 많은 사람이 한 번씩만 산 상품 → **재구매율 낮음**
        - 소수의 사람이 반복해서 산 상품 → **재구매율 높음**

        예를 들어:
        - **Bottom 상품**: 호기심 구매, 특이한 향신료, 계절 상품 등 → 단발성 구매 많음
        - **Top 상품**: 우유, 물, 간편식 등 → 정기적으로 구매하는 생활필수품

        ---

        ### 💬 마무리 포인트
        - **Bottom 10 상품**은 재구매율이 낮기 때문에  
          👉 **프로모션, 진열 변경 또는 단종 고려 대상**이 될 수 있습니다.
        - **Top 10 상품**은 충성도 높은 상품이므로  
          👉 **추천 알고리즘 반영, 할인 우선 대상** 등에 적합합니다.
        """)

    st.caption("※ 50회 이상 주문된 상품 기준")

# # 실행
# if __name__ == '__main__':
#     reorder_rate_ranking()
