import pandas as pd
import streamlit as st


def products_info():
    
    def load_data():
        products = pd.read_csv('./mydata/products.csv')
        departments = pd.read_csv('./mydata/departments.csv')
        aisles = pd.read_csv('./mydata/aisles.csv')
        id_info = pd.merge(pd.merge(products, departments, on='department_id', how='left'), aisles, on='aisle_id', how='left')[['department_id', 'department', 'aisle_id', 'aisle', 'product_id', 'product_name']]
        id_info.rename(columns={'product_id':'상품ID', 'product_name':'상품명', 'aisle_id':'세부카테고리 ID', 'aisle':'세부카테고리명', 'department_id':'카테고리 ID', 'department':'카테고리명'}, inplace=True)
        return id_info
    
    # 데이터 가져오기
    id_info = load_data()
    num_categories = id_info['카테고리명'].nunique()
    num_subcategories = id_info['세부카테고리명'].nunique()
    num_products = id_info['상품명'].nunique()

    # 키 카드
    st.markdown("### 📈 데이터 요약")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; background-color:#f0f8ff; text-align:center; box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
                <h2 style='margin:0;'>{num_categories}</h2>
                <p style='margin:0; color: gray;'>카테고리</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; background-color:#f0fff0; text-align:center; box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
                <h2 style='margin:0;'>{num_subcategories}</h2>
                <p style='margin:0; color: gray;'>세부 카테고리</p>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; background-color:#fff0f5; text-align:center; box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
                <h2 style='margin:0;'>{num_products}</h2>
                <p style='margin:0; color: gray;'>고유 상품</p>
            </div>
            """, unsafe_allow_html=True)
        
    st.markdown("---")


    st.markdown("### ⌨️ ID 검색")
    col1, col2 = st.columns(2)

    with col1:
        category_id_input = st.text_input("카테고리 ID")
        subcategory_id_input = st.text_input("세부 카테고리 ID")
        product_id_input = st.text_input("상품 ID")

    with col2:
        category_name_input = st.text_input("카테고리명")
        subcategory_name_input = st.text_input("세부 카테고리명")
        product_name_input = st.text_input("상품명")

    filtered_df = id_info.copy()
    
    # 필터 조건별로 순차적 필터링 (모두 부분일치 기준)
    if category_id_input:
        filtered_df = filtered_df[filtered_df['카테고리 ID'].astype(str).str.contains(category_id_input, case=False, na=False)]
    if category_name_input:
        filtered_df = filtered_df[filtered_df['카테고리명'].astype(str).str.contains(category_name_input, case=False, na=False)]
    if subcategory_id_input:
        filtered_df = filtered_df[filtered_df['세부카테고리 ID'].astype(str).str.contains(subcategory_id_input, case=False, na=False)]
    if subcategory_name_input:
        filtered_df = filtered_df[filtered_df['세부카테고리명'].astype(str).str.contains(subcategory_name_input, case=False, na=False)]
    if product_id_input:
        filtered_df = filtered_df[filtered_df['상품 ID'].astype(str).str.contains(product_id_input, case=False, na=False)]
    if product_name_input:
        filtered_df = filtered_df[filtered_df['상품명'].astype(str).str.contains(product_name_input, case=False, na=False)]

    # 결과 출력
    st.markdown("### 🔍 검색 결과")
    st.dataframe(filtered_df, use_container_width=True)



def buying_info():
    
    def load_data():
        data = pd.read_csv('./mydata/tmp5.csv')
        return data
    
    # 데이터 가져오기
    data = load_data()
    num_orders= data.shape[0]
    num_buying = sum(data.max_items)

    # 키 카드
    st.markdown("### 📈 데이터 요약")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; background-color:#f0f8ff; text-align:center; box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
                <h2 style='margin:0;'>{num_orders}</h2>
                <p style='margin:0; color: gray;'>누적 주문 수</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:10px; background-color:#f0fff0; text-align:center; box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
                <h2 style='margin:0;'>{num_buying}</h2>
                <p style='margin:0; color: gray;'>누적 판매 상품 수</p>
            </div>
            """, unsafe_allow_html=True)

        
    st.markdown("---")
    


