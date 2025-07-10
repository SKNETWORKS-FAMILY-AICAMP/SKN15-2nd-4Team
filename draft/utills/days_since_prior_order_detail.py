


#  이용한 data 파일 명 : orders.csv
#  이용한 column명 : order_dow, order_hour_of_day, days_since_prior_order, user_id


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib as mpl
import glob
import os



def day_hour_days_since_prior_order() :
    # 1. 리눅스 경로로 폰트 지정
    font_path = "NanumGothic-Bold.ttf"

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
    df_orders = pd.read_csv("archive/orders.csv")
    #### data5 =make_data5()
    # 요일별, 시간별 평균 주문 간격 분석
    df_orders.groupby(['order_dow', 'order_hour_of_day'])['days_since_prior_order'].mean()
    # groupby 후 평균 계산
    pivot_table = df_orders.dropna(subset=['days_since_prior_order']) \
        .groupby(['order_dow', 'order_hour_of_day'])['days_since_prior_order'] \
        .mean().reset_index().pivot(index='order_hour_of_day', columns='order_dow', values='days_since_prior_order')

    # 시각화
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("요일 + 시간대별 평균 주문 간격 (days_since_prior_order)")
    plt.xlabel("요일 (0=월요일)")
    plt.ylabel("시간 (24h 기준)")
    fig = plt.gcf()  # 현재 figure 객체를 반환
    return fig

def user_by_days_since_prior_order():
    # 1. 리눅스 경로로 폰트 지정
    font_path = "NanumGothic-Bold.ttf"

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

    # 사용자별 평균 주문 간격 계산
    #data5 =make_data5()
    df_orders = pd.read_csv("archive/orders.csv")
    df_orders.groupby('user_id')['days_since_prior_order'].mean()
    # 사용자별 평균 재주문 간격 계산
    user_avg_gap = df_orders.dropna(subset=['days_since_prior_order']) \
        .groupby('user_id')['days_since_prior_order'].mean()

    # 히스토그램 계산
    counts, bin_edges = np.histogram(user_avg_gap, bins=50)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # 데이터프레임 생성
    hist_df = pd.DataFrame({
        'avg_days_bin': bin_centers,
        'user_count': counts
    })

    # 1. bin 중심을 반올림하여 정수로 변환
    hist_df['avg_days_bin_rounded'] = hist_df['avg_days_bin'].round().astype(int)

    # 2. 사용자 수 기준으로 내림차순 정렬 후, 같은 bin은 하나만 남기기
    hist_df_unique = (
        hist_df.sort_values(by='user_count', ascending=False)
               .drop_duplicates(subset='avg_days_bin_rounded', keep='first')
    )

    # 3. 다시 사용자 수 기준으로 내림차순 정렬 (시각화용)
    hist_df_final = hist_df_unique.sort_values(by='user_count', ascending=False)

    # 4. x축을 문자열로 바꿔서 순서 유지
    hist_df_final['avg_days_bin_str'] = hist_df_final['avg_days_bin_rounded'].astype(str)

    # 5. 시각화
    plt.figure(figsize=(12, 6))
    sns.barplot(data=hist_df_final, x='avg_days_bin_str', y='user_count')
    plt.title("평균 재주문 간격별 사용자 수")
    plt.xlabel("평균 재주문 간격 (일 단위, 반올림)")
    plt.ylabel("사용자 수")
    plt.xticks(rotation=0)
    plt.tight_layout()
    fig = plt.gcf()  # 현재 figure 객체를 반환
    return fig

def user_by_days_since_prior_order_line_graph() :
        # 1. 리눅스 경로로 폰트 지정
    font_path = "NanumGothic-Bold.ttf"

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

    # 사용자별 평균 주문 간격 계산
    # data5 =make_data5()
    df_orders = pd.read_csv("archive/orders.csv")
    df_orders.groupby('user_id')['days_since_prior_order'].mean()
    # 사용자별 평균 재주문 간격 계산
    user_avg_gap = df_orders.dropna(subset=['days_since_prior_order']).groupby('user_id')['days_since_prior_order'].mean()
    counts, bin_edges = np.histogram(user_avg_gap, bins=50)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])  # 구간 중심값

    # 시각화: 꺾은선 그래프
    plt.figure(figsize=(10, 5))
    plt.plot(bin_centers, counts, marker='o', linestyle='-', color='teal')
    plt.title("사용자별 평균 주문 간격 분포 (꺾은선 그래프)")
    plt.xlabel("평균 days_since_prior_order")
    plt.ylabel("구매자 수")

    plt.grid(True)
    plt.tight_layout()
    fig = plt.gcf()  # 현재 figure 객체를 반환
    return fig


def order_dow_by_days_since_prior_order():
        # 1. 리눅스 경로로 폰트 지정
    font_path = "NanumGothic-Bold.ttf"
    
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
    
    # 요일별 평균 재주문 주기
    #data5 =make_data5()
    df_orders = pd.read_csv("archive/orders.csv")
    df_orders.groupby('order_dow')['days_since_prior_order'].mean()
    dow_avg = df_orders.dropna(subset=['days_since_prior_order']) \
    .groupby('order_dow')['days_since_prior_order'].mean()

    # 시각화
    plt.figure(figsize=(8, 5))
    sns.barplot(x=dow_avg.index, y=dow_avg.values)
    plt.title("요일별 평균 재주문 간격")
    plt.xlabel("요일 (0=월요일)")
    plt.ylabel("평균 재주문 간격")
    fig = plt.gcf()  # 현재 figure 객체를 반환
    return fig

def order_count_by_all_user():
    df_orders = pd.read_csv("archive/orders.csv")
    user_order_counts = df_orders.groupby('user_id')['order_number'].max()
    order_count_dist = user_order_counts.value_counts().sort_index()

    order_count_df = pd.DataFrame({
        'order_count': order_count_dist.index,
        'user_count': order_count_dist.values
    }).reset_index(drop=True)

    order_count_df_sorted = order_count_df.sort_values(by='user_count', ascending=False).reset_index(drop=True)
    order_count_df_sorted['순위'] = (order_count_df_sorted.index + 1).astype(str) + '위'
    order_count_df_sorted = order_count_df_sorted[['순위', 'order_count', 'user_count']]
    order_count_df_sorted.set_index('순위', inplace=True)
    order_count_df_sorted.rename(columns={
        'order_count': '총 주문 수',
        'user_count': '총 사용자 수'
    }, inplace=True)

    return order_count_df_sorted  # ✅ DataFrame 반환
