"""
products, departments 데이터 사용
대분류 별 품목 개수
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
import glob
import streamlit as st

def Product_Count_Per_Department():
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

    # 3. 데이터 불러오기
    products = pd.read_csv('./mydata/products.csv')
    departments = pd.read_csv('./mydata/departments.csv')

    # 4. 품목 수 집계
    dept_counts = products.groupby('department_id')['product_id'].nunique().reset_index()
    dept_counts.columns = ['department_id', 'product_count']

    # 5. 부서 이름 붙이기
    dept_counts = pd.merge(dept_counts, departments, on='department_id', how='left')

    # 6. 정렬
    dept_counts = dept_counts.sort_values(by='product_count', ascending=False)

    # 7. 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(dept_counts['department'][::-1], dept_counts['product_count'][::-1], color='mediumseagreen')
    ax.set_xlabel('품목 수')
    ax.set_title('부서별 등록된 품목 개수')
    for i, v in enumerate(dept_counts['product_count'][::-1]):
        ax.text(v + 10, i, str(v), va='center', fontsize=9)
    st.pyplot(fig)