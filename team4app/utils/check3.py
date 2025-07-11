import streamlit as st
import pandas as pd
from utils.data5 import make_data5
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# # 페이지 레이아웃 와이드로 설정
# st.set_page_config(layout="wide")

# 한글 폰트 설정 (윈도우)
mpl.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

@st.cache_data
def load_data_slim():
    data_full = make_data5()
    cols_needed = [
        'user_id', 'order_id', 'order_number', 'product_id',
        'product_name', 'department', 'aisle', 'days_since_prior_order', 'add_to_cart_order'
    ]
    data = data_full[cols_needed].copy()
    del data_full
    return data

def core_last_ranking(data):
    core_products = data[data['add_to_cart_order'] == 1]
    core_counts = (
        core_products.groupby(['product_id', 'product_name'])
        .size()
        .reset_index(name='첫번째_담긴_횟수')
        .sort_values('첫번째_담긴_횟수', ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    core_counts.insert(0, '순위', core_counts.index + 1)

    last_products = data.loc[data.groupby('order_id')['add_to_cart_order'].idxmax()]
    last_counts = (
        last_products.groupby(['product_id', 'product_name'])
        .size()
        .reset_index(name='마지막_담긴_횟수')
        .sort_values('마지막_담긴_횟수', ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    last_counts.insert(0, '순위', last_counts.index + 1)

    return core_counts, last_counts

def highlight_rank(s):
    color = '#cfe2f3'  # 연한 하늘색
    return [f'background-color: {color}' if col == '순위' else '' for col in s.index]

def app():
    # with st.container():
    #     st.title("🛒 첫번째/마지막 담긴 상품 Top 10 랭킹")

    data = load_data_slim()
    core_top, last_top = core_last_ranking(data)

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.subheader("첫번째 담긴 상품 Top 10")
            renamed_core = core_top.rename(columns={'product_name': '상품명'})
            styled_core = renamed_core.style.apply(highlight_rank, axis=1)
            st.dataframe(styled_core, use_container_width=True, hide_index=True)

    with col2:
        with st.container():
            st.subheader("마지막에 담긴 상품 Top 10")
            renamed_last = last_top.rename(columns={'product_name': '상품명'})
            styled_last = renamed_last.style.apply(highlight_rank, axis=1)
            st.dataframe(styled_last, use_container_width=True, hide_index=True)

    # 🎯 질문과 해설
    with st.expander("🎯 왜 첫번째와 마지막 상품이 비슷할까요? (설명 열기)", expanded=False):
        st.markdown("""
### 🎯 질문:
**왜 첫번째로 담기는 상품과 마지막에 담기는 상품이 비슷한 경우가 많을까요?**

---

### ✅ 해설:

**1. 고객 장바구니 행동의 자연스러운 흐름 때문.**

- 고객은 자주 사는 상품이나 기억하기 쉬운 상품을 **처음에 담는 경향**이 보임.  
  → 예: 바나나, 우유, 물 등은 구매 빈도가 높고, 습관처럼 바로 담게 됨.

- 반면, 장을 마무리할 때는 **놓치기 쉬운 필수품이나 보완 품목**을 마지막에 넣는 경향이 보임.  
  → 예: 과일, 생수, 간식류 등 → 빠뜨리지 않으려 끝에 추가하는 경우 많음.

---

**2. 자주 사는 상품은 '첫 담기'와 '마지막 담기' 모두에 자주 등장 가능**

- 일부 충성 고객은 **고정된 루틴**으로 장을 보며 같은 품목을 일정한 순서로 담음.  
- 그 결과, 같은 상품이 **양쪽 랭킹에 모두 등장**하는 현상이 발생.

---

**3. 구매 여정 중 반복 검색/스크롤 없이 찾기 쉬운 상품도 영향을 줌**

- 예: 바나나, 우유는 앱/웹에서 상단에 노출되거나 추천되기 쉬움 → 빠르게 선택됨.  
- 마지막에는 검색보다 **남은 예산/공간 고려**로 손에 익은 상품을 마무리로 넣을 수도 있음.

---

### 💬 시사점:

- **처음에 자주 담기는 상품** → 홈 화면, 추천 순위 상단 등에 배치하면 구매율 상승 가능  
- **마지막에 자주 담기는 상품** → 결제 직전 추천, 관련 묶음 할인 등에 활용 가치 있음  
- **양쪽에 다 있는 상품** → 핵심 충성품목 → *재고 안정, 프로모션 집중 관리 대상*
        """)

if __name__ == '__main__':
    app()
