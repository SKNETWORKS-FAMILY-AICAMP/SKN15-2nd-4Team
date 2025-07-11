import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
import glob
import streamlit as st

def Product_Count_vs_Avg_Quantity():
    # 폰트 설정 (한글 표시용)
    font_path = "./etc/NanumGothic-Bold.ttf" # 폰트 파일 경로를 정확히 지정해주세요.
    if not os.path.exists(font_path):
        print(f"Error: 폰트 파일 '{font_path}'을 찾을 수 없습니다. 폰트 경로를 확인하거나 파일을 다운로드해주세요.")
        fig = plt.figure(figsize=(12, 6))
        return fig # 빈 figure 반환

    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    mpl.font_manager.fontManager.addfont(font_path)
    mpl.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False

    # 폰트 캐시 삭제 (최초 실행 시 필요)
    cache_dir = mpl.get_cachedir()
    for cache_file in glob.glob(os.path.join(cache_dir, 'fontlist*')):
        try:
            os.remove(cache_file)
        except OSError as e:
            print(f"Error removing font cache file {cache_file}: {e}")


    # 데이터 불러오기
    try:
        order_products_prior = pd.read_csv("./mydata/order_products__prior.csv")
        products = pd.read_csv("./mydata/products.csv")
    except FileNotFoundError as e:
        print(f"Error: 데이터 파일을 찾을 수 없습니다. {e}. 'mydata' 폴더에 파일이 있는지 확인해주세요.")
        fig = plt.figure(figsize=(12, 6))
        return fig # 빈 figure 반환

    # 상품별 총 주문 수 계산
    product_total_orders = order_products_prior.groupby('product_id').size().reset_index(name='total_order_count')

    product_avg_add_to_cart_order = order_products_prior.groupby('product_id')['add_to_cart_order'].mean().reset_index(name='avg_add_to_cart_order')


    # 두 지표 병합
    product_analysis = pd.merge(product_total_orders, product_avg_add_to_cart_order, on='product_id', how='left')

    # 상품 이름 병합
    product_analysis = pd.merge(product_analysis, products[['product_id', 'product_name']], on='product_id', how='left')

    # 시각화
    plt.figure(figsize=(12, 8))
    plt.scatter(product_analysis['total_order_count'], product_analysis['avg_add_to_cart_order'], alpha=0.6, s=10) # s는 점 크기
    plt.title('상품별 총 주문 수 vs. 평균 카트 담김 순서')
    plt.xlabel('총 주문 수')
    plt.ylabel('평균 카트 담김 순서 (한 주문 내)') # '평균 주문 수량'의 대리 지표임을 명시
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig = plt.gcf()
    return fig

# # Streamlit 앱에 통합 (예시)
# if __name__ == '__main__':
    
#     st.set_page_config(layout="wide")
#     st.title("🛍️ 상품 분석: 주문 수량 관계")
#     fig_scatter = Product_Count_vs_Avg_Quantity()
#     st.pyplot(fig_scatter)

