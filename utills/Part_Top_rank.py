import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import numpy as np
import matplotlib.font_manager as fm
import matplotlib as mpl
import glob
from data5 import make_data5

def PART_List():
    # 1. 리눅스 경로로 폰트 지정
    font_path = "../NanumGothic-Bold.ttf"

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

    data5 = make_data5()

    # 상품 분류
    grouped_product = pd.DataFrame(data5.groupby(['department', 'aisle_id'])['product_name'].unique())
    grouped_product = grouped_product.reset_index()

    # product_name 리스트 풀기
    grouped_product = grouped_product.explode('product_name')

    product_count = grouped_product.groupby('department')['product_name'].count().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    product_count.plot(kind='barh', color='blue')
    plt.title('대분류별 상품 목록 수')
    plt.xlabel('상품 수')
    plt.ylabel('대분류 이름')
    plt.tight_layout()
    plt.show()

def PART_Dataframe():
    data5 = make_data5()
    # 상품 분류
    grouped_product = pd.DataFrame(data5.groupby(['department', 'aisle_id'])['product_name'].unique())
    grouped_product = grouped_product.reset_index()

    # product_name 리스트 풀기
    grouped_product = grouped_product.explode('product_name')

    product_count = pd.DataFrame(grouped_product.groupby('department')['product_name'].count().sort_values(ascending=False))

    product_count=product_count.reset_index()
    product_count = product_count.rename(columns={'department':'상품 대분류','product_name':'상품 개수'})
    # 기존 인덱스를 랭킹으로 사용하고, 인덱스 제거
    product_count = product_count.reset_index(drop=True)  # 인덱스 초기화
    product_count['순위'] = (product_count.index + 1).astype(str) + '위'      # 1부터 시작하는 랭킹 컬럼 추가

    # 컬럼 순서 조정 (선택 사항)
    product_count = product_count[['순위', '상품 대분류', '상품 개수']]
    product_count.set_index('순위', inplace=True)
    return(product_count)
