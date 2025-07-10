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

# 페이지 기본 설정
st.set_page_config(
    page_title="가입 고객 이탈 예측",
    page_icon="🛒",
    layout="wide"
)

st.set_page_config(layout="wide")

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
                            icons=['house', 'graph-down', 'tags', 'basket', 'megaphone'], 
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
    customer_info()

# 2. PAGE:
if main_selected==menu_list[1]:
    st.title('📈 이탈 가능성 분석')
    model_explain()




# 3. PAGE:
if main_selected==menu_list[2]:
    st.title('🏷️ InstaCart 상품 통계 시각화')
    list_products = ['상품 관리', '상품 분석']
    # 보조 메뉴
    selected_products = option_menu(None, list_products, 
        icons=['box-seam', 'ui-checks-grid'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                "nav-link-selected": {"background-color": "#ffb867"}
                })
    
    if selected_products==list_products[0]:
        products_info()

    # st.subheader("📦 카테고리별 상품 종류")
    # fig_products_per_department = Product_Count_Per_Department()
    # st.pyplot(fig_products_per_department)

    # if selected_products==list_products[1]:
    #     st.header("고객 선호도 및 부서별 상품 정보를 시각화한 결과")
    #     # 🎯 상단 2개 그래프: 좌우 분할
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.subheader("🔺 Top 10 Products by Percent")
    #         fig_products_rank = Products_Rank()
    #         st.pyplot(fig_products_rank)

    #     with col2:
    #         pass

    #     st.markdown("---")
    #     st.subheader("🌟 Top 20 Most Ordered Products")
    #     fig_products_under_rank = Products_Under_Rank()
    #     st.pyplot(fig_products_under_rank)

    #     st.subheader("📌 인기 상품명 워드 클라우드 분석")
    #     fig_wordcloud = Product_Name_Word_Cloud()
    #     st.pyplot(fig_wordcloud)
    #     st.markdown("---")

    #     st.subheader('📌 상품 분석: 주문 수량 관계')
    #     fig_scatter = Product_Count_vs_Avg_Quantity()
    #     st.pyplot(fig_scatter)
    #     st.markdown("---")




# 4. PAGE:
if main_selected==menu_list[3]:
    st.title('🛒 InstaCart 구매 행동 분석 대시보드')
    list_buying = ['주문 관리','시간/재주문', '', '']
    # 보조 메뉴
    selected_buying = option_menu(None, list_buying, 
        icons=['calendar', 'calendar-day', ''], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "black"},
                "nav-link-selected": {"background-color": "#ffb867"}
                })

    if selected_buying==list_buying[0]:
        buying_info()

    if selected_buying==list_buying[1]:
        # 📌 1. 요일 + 시간대별 평균 주문 간격
        st.subheader("📌 요일 + 시간대별 평균 주문 간격 (히트맵)")
        st.markdown("주문 간격의 평균이 요일과 시간에 따라 어떻게 달라지는지 시각화")
        fig1 = day_hour_days_since_prior_order()
        st.pyplot(fig1)
        st.markdown("전체적으로 오전 0~6시 재구매 간격이 가장 길게 평가되고, 월,화수,일요일 보다는 목,금,토요일에 재구매 율이 높게 평가됨.")        
        st.markdown("---")
        
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

        # 📌 3. 요일별 평균 재주문 간격
        st.subheader("📌 요일별 평균 재주문 간격")
        st.markdown("요일에 따라 재주문 간격이 어떻게 달라지는지 시각화한 막대그래프입니다.")
        fig4 = order_dow_by_days_since_prior_order()
        st.pyplot(fig4)
        st.markdown("""
                    - 재주문 간격은 요일에 크게 영향을 받지 않는다는 것을 확인 할 수 있다.
                    """)
        st.markdown("---")

        # 📌 4. 사용자별 총 주문 횟수 순위
        st.subheader("📌 사용자별 총 주문 횟수 순위 (Top 10)")
        st.markdown("총 주문 횟수 기준으로 사용자 수가 많은 순으로 정리한 테이블입니다.")
        df = order_count_by_all_user()
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("---")


    if selected_buying==list_buying[2]:
        pass


# 5. PAGE:
if main_selected==menu_list[4]:
    st.title('🔎 고객별 분석')