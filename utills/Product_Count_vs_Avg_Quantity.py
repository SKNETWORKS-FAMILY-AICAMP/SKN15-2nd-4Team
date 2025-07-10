import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os
import glob

def Product_Count_vs_Avg_Quantity():
    # 폰트 설정 (한글 표시용)
    font_path = "./NanumGothic-Bold.ttf" # 폰트 파일 경로를 정확히 지정해주세요.
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

    # 데이터 불러오기
    try:
        order_products_prior = pd.read_csv("./mydata/order_products__prior.csv")
        products = pd.read_csv("./mydata/products.csv")
    except FileNotFoundError as e:
        print(f"Error: 데이터 파일을 찾을 수 없습니다. {e}. 'mydata' 폴더에 파일이 있는지 확인해주세요.")
        return plt.figure()

    # 상품별 총 주문 수 계산
    product_total_orders = order_products_prior.groupby('product_id').size().reset_index(name='total_order_count')

    # 상품별 평균 주문 수량 계산
    # 'reordered' 컬럼을 이용하여 각 주문에서 해당 상품이 몇 개 포함되었는지 추정합니다.
    # Instacart 데이터셋의 'reordered'는 상품이 이전에 주문된 적 있는지 여부이므로,
    # 정확한 '수량' 정보는 'add_to_cart_order' 컬럼을 활용하거나,
    # 해당 데이터셋에 명시적인 'quantity' 컬럼이 없으면 단순 1개로 가정하고 진행해야 합니다.
    # 여기서는 'product_id'별로 'order_id'의 수를 총 주문수로 보고, 각 주문 건당 해당 상품이 추가된 횟수를 1로 가정하여 진행합니다.
    # 만약 'order_products__prior'에 명시적인 상품 수량(quantity) 컬럼이 있다면 해당 컬럼을 사용해야 합니다.
    # 이 데이터셋에는 각 주문에 상품이 '추가되었는지'만 기록되어 있으므로,
    # '평균 주문 수량'은 'product_id'별로 'add_to_cart_order'의 평균으로 간주하거나,
    # 각 주문에 이 상품이 '추가된' 횟수를 1로 보고 단순 '재구매율'과 혼동될 수 있습니다.
    # 여기서는 좀 더 직관적인 해석을 위해 'add_to_cart_order'를 평균 수량의 대리 지표로 사용하거나,
    # 단순히 '상품이 포함된 총 주문 수'를 사용하겠습니다.
    # 만약 실제 '수량' 데이터가 있다면 훨씬 더 정확한 분석이 가능합니다.

    # 임시적으로 각 주문에 해당 상품이 '한 번' 포함되었다고 가정하고,
    # 단순히 주문 횟수당 평균을 계산하여 '평균 구매 빈도'와 같은 개념으로 접근하겠습니다.
    # 보다 정확한 '평균 수량'을 위해서는 주문 내 개별 상품 수량 컬럼이 필요합니다.

    # 여기서는 각 product_id가 포함된 전체 order_products__prior 레코드 수를 '총 구매 횟수'로 사용하고,
    # 'add_to_cart_order'는 장바구니에 담긴 순서이므로, 이 데이터셋에서 '평균 수량'을 직접적으로 도출하기 어렵습니다.
    # 따라서, '평균 주문 수량' 대신 '상품이 포함된 평균 카트 순서'나 다른 의미로 해석하거나
    # '총 주문 수'만으로 분석하는 것이 적절할 수 있습니다.
    # 하지만 요청에 따라 '평균 주문 수량'의 의미를 찾기 위해,
    # 각 상품이 개별 주문에 포함될 때의 'add_to_cart_order'의 평균을 사용해보겠습니다.
    # 이는 '하나의 주문 내에서 평균적으로 몇 번째로 카트에 담겼는지'를 의미하며 '수량'과는 다릅니다.

    # 실제 '수량' 컬럼이 없음을 고려하여,
    # '평균 주문 수량'을 '한 주문에서 해당 상품이 평균적으로 몇 개 들어갔는지'가 아닌,
    # '해당 상품이 포함된 주문의 평균 카트 담김 순서'로 해석하겠습니다.
    # 이 방법이 데이터의 한계 내에서 가장 합리적인 시도입니다.
    product_avg_add_to_cart_order = order_products_prior.groupby('product_id')['add_to_cart_order'].mean().reset_index(name='avg_add_to_cart_order')


    # 두 지표 병합
    product_analysis = pd.merge(product_total_orders, product_avg_add_to_cart_order, on='product_id', how='left')

    # 상품 이름 병합
    product_analysis = pd.merge(product_analysis, products[['product_id', 'product_name']], on='product_id', how='left')

    # 시각화
    plt.figure(figsize=(12, 8))
    plt.scatter(product_analysis['total_order_count'], product_analysis['avg_add_to_cart_order'], alpha=0.6, s=10) # s는 점 크기
    plt.xlabel('총 주문 수')
    plt.ylabel('평균 카트 담김 순서 (한 주문 내)') # '평균 주문 수량'의 대리 지표임을 명시
    plt.title('상품별 총 주문 수 vs. 평균 카트 담김 순서')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    fig = plt.gcf()
    return fig

# Streamlit 앱에 통합 (예시)
if __name__ == '__main__':
    import streamlit as st
    st.set_page_config(layout="wide")
    st.title("🛍️ 상품 분석: 주문 수량 관계")

    st.write("### 상품별 총 주문 수 vs. 평균 카트 담김 순서 산점도")
    st.write("데이터셋의 한계로 인해 '평균 주문 수량' 대신 '평균 카트 담김 순서'를 지표로 사용했습니다. 이는 '하나의 주문 내에서 평균적으로 몇 번째로 장바구니에 담겼는지'를 나타냅니다.")
    fig_scatter = Product_Count_vs_Avg_Quantity()
    st.pyplot(fig_scatter)