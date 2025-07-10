import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm
import os
import glob
import matplotlib as mpl

def Product_Name_Word_Cloud():
    # 폰트 설정 (한글 표시용)
    font_path = "./NanumGothic-Bold.ttf" # 폰트 파일 경로를 정확히 지정해주세요.
    # 만약 폰트 파일이 없다면 다운로드하여 현재 디렉토리 또는 시스템 폰트 경로에 넣어주세요.
    # 예시 다운로드 링크: https://github.com/naver/nanumfont

    if not os.path.exists(font_path):
        print(f"Error: 폰트 파일 '{font_path}'을 찾을 수 없습니다. 폰트 경로를 확인하거나 파일을 다운로드해주세요.")
        return plt.figure() # 빈 figure 반환

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
    # 폰트 캐시를 지운 후에는 폰트가 바로 적용되지 않을 수 있으니,
    # 가능하다면 Jupyter/IDE를 재시작하는 것이 좋습니다.

    # 데이터 불러오기
    try:
        order_products__prior = pd.read_csv("./mydata/order_products__prior.csv")
        products = pd.read_csv("./mydata/products.csv")
    except FileNotFoundError as e:
        print(f"Error: 데이터 파일을 찾을 수 없습니다. {e}. 'mydata' 폴더에 파일이 있는지 확인해주세요.")
        return plt.figure()

    # 상품별 주문 수 집계
    product_orders_count = order_products__prior['product_id'].value_counts().reset_index()
    product_orders_count.columns = ['product_id', 'order_count']

    # 상품명과 병합
    product_popularity = pd.merge(product_orders_count, products[['product_id', 'product_name']], on='product_id', how='left')

    # 인기도가 높은 상품명으로 텍스트 데이터 생성
    # 각 상품명을 주문 수만큼 반복하여 텍스트 데이터로 만듭니다.
    # 이렇게 하면 더 많이 주문된 상품의 이름이 워드 클라우드에서 더 크게 표시됩니다.
    text_data = ""
    for index, row in product_popularity.iterrows():
        text_data += (row['product_name'] + " ") * int(row['order_count'] / 100) # 적절한 가중치 조절

    if not text_data:
        print("워드 클라우드를 생성할 텍스트 데이터가 부족합니다.")
        return plt.figure()

    # 워드 클라우드 생성 설정
    wc = WordCloud(
        font_path=font_path, # 한글 폰트 경로 지정
        width=1200,
        height=800,
        background_color='white',
        max_words=100, # 최대 단어 수
        min_font_size=10,
        colormap='viridis' # 색상 맵
    ).generate(text_data)

    # 워드 클라우드 시각화
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off') # 축 제거
    plt.title('인기 상품명 워드 클라우드')
    plt.tight_layout()
    fig = plt.gcf()
    return fig

# Streamlit 앱에 통합 (예시)
if __name__ == '__main__':
    import streamlit as st
    st.set_page_config(layout="wide")
    st.title("🛍️ 상품명 워드 클라우드 분석")

    st.write("### 인기 상품명 워드 클라우드")
    fig_wordcloud = Product_Name_Word_Cloud()
    st.pyplot(fig_wordcloud)