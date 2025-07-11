import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
import glob
import streamlit as st


def first_order_products():
    # 1. 폰트 설정 (한글 표시용)
    font_path = "./etc/NanumGothic-Bold.ttf"
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    mpl.font_manager.fontManager.addfont(font_path)
    mpl.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False

    # 2. 캐시 삭제 (최초만)
    cache_dir = mpl.get_cachedir()
    for cache_file in glob.glob(os.path.join(cache_dir, 'fontlist*')):
        os.remove(cache_file)

    orders_df = pd.read_csv("./mydata/orders.csv")
    order_products_df = pd.read_csv('./mydata/order_products__prior.csv')
    products_df = pd.read_csv('./mydata/products.csv')


    # 각 사용자의 첫 번째 주문을 찾습니다. (order_number가 1인 주문)
    first_orders = orders_df[orders_df['order_number'] == 1]

    # 첫 주문과 주문-상품 데이터를 병합하여 첫 주문에 포함된 상품들을 식별합니다.
    # 'order_id'를 기준으로 병합합니다.
    first_order_products = pd.merge(first_orders,
                                    order_products_df,
                                    on='order_id',
                                    how='inner')


    # 첫 주문 상품 데이터와 상품 정보를 병합하여 상품 이름을 가져옵니다.
    first_order_products_with_names = pd.merge(first_order_products,
                                                    products_df[['product_id', 'product_name']],
                                                    on='product_id',
                                                    how='left')

    # 각 상품별로 첫 주문에 포함된 횟수를 집계합니다.
    first_order_product_counts = first_order_products_with_names['product_name'].value_counts().reset_index()
    first_order_product_counts.columns = ['product_name', 'first_order_count']

    # 첫 주문 횟수 기준으로 내림차순 정렬
    first_order_product_counts = first_order_product_counts.sort_values(by='first_order_count', ascending=False)
    first_order_product_counts= first_order_product_counts.head(10)

    fig, ax = plt.subplots(figsize=(12, max(6, len(first_order_product_counts) * 0.5))) # 최소 높이 6, 항목 수에 따라 동적 조절

    ax.barh(
        first_order_product_counts['product_name'][::-1],
        first_order_product_counts['first_order_count'][::-1],
        color='cornflowerblue' # 막대 색상
    )

    # 라벨, 제목 설정 (ax 객체 사용)
    ax.set_xlabel('첫 주문 횟수', fontsize=12)
    ax.set_ylabel('상품명', fontsize=12)
    ax.set_title('고객들이 첫 주문으로 많이 선택한 상품 (상위 10개)', fontsize=15) # 상위 10개임을 명시

    # 각 막대 옆에 값 표시 (ax 객체 사용)
    for i, v in enumerate(first_order_product_counts['first_order_count'][::-1]):
        ax.text(v + 10, i, str(v), va='center', fontsize=9) # 텍스트 위치 조정

    ax.grid(axis='x', linestyle='--', alpha=0.7) # x축 그리드 라인 추가
    plt.tight_layout() # 그래프 요소들이 잘 맞도록 자동 조정
    st.pyplot(fig)

