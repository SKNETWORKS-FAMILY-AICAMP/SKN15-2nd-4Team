import streamlit as st
from streamlit_option_menu import option_menu
from utils.days_since_prior_order_detail import (
    day_hour_days_since_prior_order,
    user_by_days_since_prior_order,
    user_by_days_since_prior_order_line_graph,
    order_dow_by_days_since_prior_order,
    order_count_by_all_user,
)
from utils.Products_Rank import (
    Products_Rank,
    Products_Under_Rank,
    )
from utils.Part_Top_rank import Product_Count_Per_Department
from utils.Product_Count_vs_Avg_Quantity import Product_Count_vs_Avg_Quantity
from utils.Product_Name_Word_Cloud import Product_Name_Word_Cloud
from utils.data_info import products_info, buying_info
from utils.model import model_explain
from utils.customer_info import customer_info
from utils.check import due_date_churn
from utils.check2 import reorder_rate_ranking
from utils.check3 import app
from utils.mj import mj_buying, mj_reorder, mj_royalty
from utils.first_order_products import first_order_products
from utils.month_need import month_need
from utils.streamlit_membership_grade import main
from utils.list import membership_churn

service_name="가입 고객 이탈 예측"
# 페이지 기본 설정
st.set_page_config(
    page_title=service_name,
    page_icon="🛒",
    layout="wide"
)

# 스타일 설정 (글씨체/색상/정렬)
st.markdown("""
    <style>
    /* 메인 메뉴 타이틀 */
    .sidebar-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a7ee6;  /* 원하는 색상 */
        padding: 10px 0 5px 15px;  /* 약간 왼쪽 들여쓰기 */
    }

    /* 오른쪽 정렬용 */
    .sidebar-footer {
        text-align: right;
        padding: 20px 15px 0 0;
        font-size: 13px;
        color: #999999;
    }
    </style>
""", unsafe_allow_html=True)


# 메뉴 구성
# icon 참고: https://icons.getbootstrap.com/?q=power
menu_list=["홈", "이탈 가능성 분석", "상품별 분석", '구매별 분석', '고객별 분석']
with st.sidebar:
    st.title("메뉴")
    main_selected = option_menu("", menu_list, 
                            icons=['house', 'graph-down', 'box', 'tags', 'basket', 'megaphone'], 
                            menu_icon="list", 
                            default_index=0,
                            styles={
                            "container": {"padding": "0!important", "background-color": "#fafafa"},
                            "icon": {"color": "black", "font-size": "20px"},
                            "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                            "nav-link-selected": {"background-color": "#a3dfff"}
                            })
    st.markdown('<div class="sidebar-footer">Made By. 내물품좀4조  @2025.07.</div>', unsafe_allow_html=True)

# 1. PAGE: HOME
if main_selected==menu_list[0]:
    st.set_page_config(
    page_title=f"홈:{service_name}",
    page_icon="🛒",
    layout="wide"
    )
    st.title('🏠 전체 요약')
    customer_info()
    membership_churn()

# 2. PAGE:
if main_selected==menu_list[1]:
    st.set_page_config(
    page_title=f"이탈분석:{service_name}",
    page_icon="🛒",
    layout="wide"
    )
    st.title('📈 이탈 가능성 분석')
    list_churn = ['모델 설명', '이탈 가능성 정의', '이탈 분석']
    # 보조 메뉴
    selected_churn = option_menu(None, list_churn, 
        icons=['box-seam', 'ui-checks-grid', 'ui-checks-grid'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
                "container": {
                    "padding": "0!important", 
                    "background-color": "#fafafa",
                    },
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {"font-size": "18px", 
                            "text-align": "left", 
                            "margin":"0px", 
                            "--hover-color": "#eee", 
                            "color": "black"},
                "nav-link-selected": {"background-color": "#ffb867"},
                "nav":{"justify-content":'flex-start'}
                })
    
    if selected_churn==list_churn[0]:
        model_explain()

    if selected_churn==list_churn[1]:
        pass
        
    if selected_churn==list_churn[2]:
        due_date_churn()
        mj_royalty()
        
        

# 3. PAGE:
if main_selected==menu_list[2]: 
    st.set_page_config(
    page_title=f"상품분석:{service_name}",
    page_icon="🛒",
    layout="wide"
    )
    st.title('🏷️ InstaCart 상품 통계 시각화')
    list_products = ['상품 관리', '총 판매량 TOP', "첫 구매 TOP", "재구매율 TOP", "장바구니 순서 TOP"]
    # 보조 메뉴
    selected_products = option_menu(None, list_products, 
        icons=['box-seam', 'box-seam', 'box-seam', 'box-seam', 'box-seam'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                "nav-link-selected": {"background-color": "#ffb867"}
                })
    
    if selected_products==list_products[0]:
        st.subheader("📌 상품 관리")
        products_info()

        Product_Count_Per_Department()
        

    if selected_products==list_products[1]:
        st.subheader("📌 총 판매량 TOP 상품")
        buying_info()
        Products_Rank()
        Products_Under_Rank()
        
        st.subheader("📌 인기 상품명 워드 클라우드 분석")
        fig_wordcloud = Product_Name_Word_Cloud()
        st.pyplot(fig_wordcloud)
        

    if selected_products==list_products[2]:
        st.subheader("📌 첫 구매 TOP 상품")
        first_order_products()

    if selected_products==list_products[3]:
        st.subheader("📌 재구매율 TOP 상품")
        reorder_rate_ranking()  

    if selected_products==list_products[4]:
        st.subheader("📌 장바구니 순서 TOP 상품")
        app()


# 4. PAGE:
if main_selected==menu_list[3]:
    st.set_page_config(
    page_title=f"구매분석:{service_name}",
    page_icon="🛒",
    layout="wide"
    )
    st.title('🛒 InstaCart 구매 행동 분석 대시보드')
    list_buying = ['요일/시간', '재주문', '주문 수량', '구매 주기']
    # 보조 메뉴
    selected_buying = option_menu(None, list_buying, 
        icons=['calendar-day', 'calendar', 'calendar', 'calendar'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                "nav-link-selected": {"background-color": "#ffb867"}
                })

    if selected_buying==list_buying[0]:
        # 📌 1. 요일 + 시간대별 평균 주문 간격
        st.subheader("📌 요일 + 시간대별 평균 주문 간격 (히트맵)")
        st.markdown("주문 간격의 평균이 요일과 시간에 따라 어떻게 달라지는지 시각화")
        fig1 = day_hour_days_since_prior_order()
        st.pyplot(fig1)
        st.markdown("전체적으로 오전 0~6시 재구매 간격이 가장 길게 평가되고, 월,화수,일요일 보다는 목,금,토요일에 재구매 율이 높게 평가됨.")        
        st.markdown("---")

        # 📌 3. 요일별 평균 재주문 간격
        st.subheader("📌 요일별 평균 재주문 간격")
        st.markdown("요일에 따라 재주문 간격이 어떻게 달라지는지 시각화한 막대그래프입니다.")
        fig4 = order_dow_by_days_since_prior_order()
        st.pyplot(fig4)
        st.markdown("""
                    - 재주문 간격은 요일에 크게 영향을 받지 않는다는 것을 확인 할 수 있다.
                    """)
        st.markdown("---")

    if selected_buying==list_buying[1]:    
        # 📌 2. 평균 재주문 간격별 사용자 수 - 막대 + 꺾은선
        st.subheader("📌 평균 재주문 간격별 사용자 수")
        st.markdown("- 사용자별 평균 재주문 간격 분포 시각화")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**• 막대그래프**")
            fig2 = user_by_days_since_prior_order()
            st.pyplot(fig2)
            st.markdown("""
                        - 평균 재주문 간격별 사용자 수를 내림차순으로 정리
                        - 가장 높은 사용자들은 7~17일 주기로 재주문
                        """)
        with col2:
            st.markdown("**• 꺾은선 그래프**")
            fig3 = user_by_days_since_prior_order_line_graph()
            st.pyplot(fig3)
            st.markdown("""
                        - 평균 간격 약 7~17일 사이에 많은 사용자가 재주문
                        """)
        st.markdown("---")

        mj_reorder()
        st.markdown("---")

    if selected_buying==list_buying[2]:
        st.subheader('📌 상품과 주문 수량 관계')
        fig_scatter = Product_Count_vs_Avg_Quantity()
        st.pyplot(fig_scatter)
        st.markdown("""
                    - 상품 판매 수와 장바구니에 담기는 순서의 영향성 파악 표현
                    - 인사이트
                        - 인기 상품은 소수이고, 대부분의 상품은 인기가 많지 않습니다. 
                        - 매우 인기 있는 상품(총 주문 수가 높은)일수록 장바구니에 초반에 담기는 경향이 강합니다. (오른쪽으로 갈수록 점들이 Y축 낮은 곳에 모이는 경향이 있음)
                        - 인기가 없는 상품들은 장바구니에 담기는 순서가 매우 다양할 수 있습니다. (왼쪽 영역에서 Y축으로 점들이 흩어져 있음)
                    """)
        st.markdown("---")        

        # 📌 4. 사용자별 총 주문 횟수 순위
        st.subheader("📌 사용자별 총 주문 횟수 순위 (Top 10)")
        st.markdown("총 주문 횟수 기준으로 사용자 수가 많은 순으로 정리한 테이블입니다.")
        df = order_count_by_all_user()
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("---")

    if selected_buying==list_buying[3]:
        mj_buying()

# 5. PAGE:
if main_selected==menu_list[4]:
    st.set_page_config(
    page_title=f"고객분석:{service_name}",
    page_icon="🛒",
    layout="wide"
    )
    st.title('🔎 고객별 분석')
    main()
    