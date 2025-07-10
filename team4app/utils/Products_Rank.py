"""
order_products__prior, products 데이터 사용
상품 인기 순위 TOP10, BOTTOM10
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import glob
import os

def Products_Rank():
    # 1. 폰트 지정
    font_path = "./etc/NanumGothic-Bold.ttf"

    # 2. 폰트 등록 및 적용
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    mpl.font_manager.fontManager.addfont(font_path)
    mpl.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False

    # 3. 폰트 캐시 삭제(최초 적용 시)
    cache_dir = mpl.get_cachedir()
    for cache_file in glob.glob(os.path.join(cache_dir, 'fontlist*')):
        os.remove(cache_file)

    # 1. 데이터 준비
    order_products__prior = pd.read_csv("./mydata/order_products__prior.csv")
    products = pd.read_csv("./mydata/products.csv")

    # 2. 주문 수 집계
    product_orders = order_products__prior.groupby('product_id')['order_id'].count().reset_index()
    product_orders.columns = ['product_id', 'order_count']

    # 3. 상품 이름 붙이기
    product_orders = pd.merge(product_orders, products[['product_id', 'product_name']], on='product_id', how='left')

    # 4. 주문 수 기준 정렬
    top10 = product_orders.sort_values(by='order_count', ascending=False).head(10)

    # 5. 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(top10['product_name'][::-1], top10['order_count'][::-1], color='orange')
    ax.set_xlabel('총 주문 수')
    ax.set_title('구매 품목 TOP 10')

    # 6. 막대 위에 숫자 표시
    for i, v in enumerate(top10['order_count'][::-1]):
        ax.text(v + 100, i, str(v), va='center', fontsize=9)

    fig.tight_layout()

    return fig


def Products_Under_Rank():
    # 1. 리눅스 경로로 폰트 지정
    font_path = "./etc/NanumGothic-Bold.ttf"

    # 2. 폰트 등록 및 적용
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    mpl.font_manager.fontManager.addfont(font_path)
    mpl.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False

    # 3. 폰트 캐시 삭제(최초 적용 시)
    cache_dir = mpl.get_cachedir()
    for cache_file in glob.glob(os.path.join(cache_dir, 'fontlist*')):
        os.remove(cache_file)

    # 1. 데이터 준비
    order_products__prior = pd.read_csv("./mydata/order_products__prior.csv")
    products = pd.read_csv("./mydata/products.csv")

    # 2. 주문 수 집계
    product_orders = order_products__prior.groupby('product_id')['order_id'].count().reset_index()
    product_orders.columns = ['product_id', 'order_count']

    # 3. 상품 이름 붙이기
    product_orders = pd.merge(product_orders, products[['product_id', 'product_name']], on='product_id', how='left')

    bottom10 = product_orders.sort_values(by='order_count', ascending=True).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(bottom10['product_name'], bottom10['order_count'], color='lightcoral')
    plt.xlabel('총 주문 수')
    plt.title('구매 품목 하위 10')
    for i, v in enumerate(bottom10['order_count']):
        plt.text(v + 1, i, str(v), va='center', fontsize=9)
    plt.tight_layout()
    fig = plt.gcf()
    return fig
