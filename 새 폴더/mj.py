# mj.py
# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# def render_dashboard():
#     # --- 데이터 불러오기 ---
#     @st.cache_data
#     def load_data():
#         df = pd.read_csv('./pages/functions/user_pattern.csv')
#         return df

#     df = load_data()
#     user_pattern = load_data()

#     # --- 1단계: 평균 구매 주기 분석 ---
#     st.header("1. 평균 구매 주기 분석 → 루틴과 이탈 경향 파악")

#     st.markdown("""
#     - **의미**: 고객이 플랫폼에 얼마나 자주 방문하고 있는지 보여주는 지표
#     - **인사이트**:
#         - 평균 주기가 **20일 이상인 고객**은 이탈 위험이 상대적으로 높음
#         - 평균 주기가 짧은 고객은 **루틴하게 사용하는 충성 고객 가능성**
#     """)

#     fig1, ax1 = plt.subplots(figsize=(8, 4))
#     sns.histplot(user_pattern['avg_order_interval'], bins=30, kde=True, color='skyblue', ax=ax1)
#     plt.axvline(x=20, color='red', linestyle='--', label='이탈 경계선 예시')
#     plt.title('고객 평균 주문 주기 분포')
#     plt.xlabel('평균 주문 주기 (일)')
#     plt.ylabel('고객 수')
#     plt.legend()
#     plt.grid(True)
#     st.pyplot(fig1)

#     # --- 2단계: 평균 주문 수 분석 ---
#     st.header("2. 평균 주문 수 분석 → 충성도, LTV 추정")

#     st.markdown("""
#     - **의미**: 고객이 플랫폼에서 얼마나 자주, 많이 주문했는지를 보여주는 지표
#     - **인사이트**:
#         - 평균보다 많이 주문한 고객은 충성도가 높고 VIP로 볼 수 있음
#         - 주문 수가 적은 고객은 신규/이탈 위험 가능성
#     """)

#     fig2, ax2 = plt.subplots(figsize=(8, 4))
#     sns.histplot(user_pattern['total_orders'], bins=30, color='mediumseagreen', ax=ax2)
#     plt.axvline(user_pattern['total_orders'].mean(), color='red', linestyle='--', label=f"평균 주문 수: {user_pattern['total_orders'].mean():.2f}")
#     plt.yscale('log')
#     plt.title('고객 총 주문 수 분포 (Log Scale)')
#     plt.xlabel('총 주문 수')
#     plt.ylabel('고객 수 (로그)')
#     plt.legend()
#     plt.grid(True)
#     st.pyplot(fig2)

#     # --- 3단계: 재주문 비율 분석 ---
#     st.header("3. 전체 재주문 비율 분석 → 반복구매 성향, 제품 만족도")

#     st.markdown("""
#     - **의미**: 고객이 같은 제품을 반복 구매하는 경향성 (충성도 높은 고객 확인 가능)
#     - **인사이트**:
#         - 재주문 비율이 0.7 이상이면 제품/플랫폼에 대한 만족도가 높음
#         - 0.4 이하면 충성도 낮음 또는 일회성 이용 가능성
#     """)

#     fig3, ax3 = plt.subplots(figsize=(8, 4))
#     sns.kdeplot(user_pattern['reorder_ratio'], fill=True, color='orange', ax=ax3)
#     plt.axvline(user_pattern['reorder_ratio'].mean(), color='red', linestyle='--', label='전체 평균')
#     plt.title('고객 재주문 비율 분포')
#     plt.xlabel('재주문 비율')
#     plt.ylabel('밀도')
#     plt.legend()
#     plt.grid(True)
#     st.pyplot(fig3)

#     # --- 4. 주문 수 vs 재주문 비율 산점도 ---
#     st.header("4. 고객 유형 관계 시각화")

#     fig4, ax4 = plt.subplots(figsize=(8, 6))
#     sns.scatterplot(data=user_pattern, x='total_orders', y='reorder_ratio', alpha=0.5, ax=ax4)
#     plt.axvline(20, color='red', linestyle='--', label='충성 고객 기준 (20회 이상)')
#     plt.axhline(0.7, color='orange', linestyle='--', label='재주문율 기준 (70% 이상)')
#     plt.title('총 주문 수 vs 재주문 비율')
#     plt.xlabel('총 주문 수')
#     plt.ylabel('재주문 비율')
#     plt.legend()
#     plt.grid(True)
#     st.pyplot(fig4)

#     # --- 5. 충성도 세그먼트 분류 시각화 ---
#     st.header("5. 고객 충성도 세그먼트 분포")

#     def classify_customer(row):
#         if row['total_orders'] >= 20 and row['reorder_ratio'] >= 0.7:
#             return 'VIP 충성 고객'
#         elif row['total_orders'] >= 10 and row['reorder_ratio'] >= 0.5:
#             return '일반 충성 고객'
#         elif row['total_orders'] < 10 and row['reorder_ratio'] < 0.4:
#             return '이탈 위험군'
#         else:
#             return '기타'

#     user_pattern['loyalty_segment'] = user_pattern.apply(classify_customer, axis=1)

#     fig5, ax5 = plt.subplots()
#     user_pattern['loyalty_segment'].value_counts().plot(kind='bar', color='cornflowerblue', ax=ax5)
#     plt.title('고객 충성도 세그먼트 분포')
#     plt.ylabel('고객 수')
#     plt.xticks(rotation=0)
#     plt.grid(True)
#     st.pyplot(fig5)

#     # --- 6. 충성도별 평균 지표 비교 ---
#     st.header("6. 충성도 등급별 평균 지표 비교")

#     avg_metrics = user_pattern.groupby('loyalty_segment')[['avg_order_interval', 'total_orders', 'reorder_ratio']].mean().round(2)
#     st.dataframe(avg_metrics)
# ===================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("📊 고객 구매 패턴 분석 대시보드")

# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    df = pd.read_csv('./pages/functions/user_pattern.csv')
    return df

user_pattern = load_data()

# --- 요약 통계 표시 ---
st.subheader("📌 고객 주문 수 통계 요약")
summary_stats = user_pattern['total_orders'].describe().round(2)
st.dataframe(summary_stats.rename("값"))

# --- 1단계: 평균 구매 주기 분석 ---
st.header("1. 평균 구매 주기 분석 → 루틴과 이탈 경향 파악")

st.markdown("""
- **의미**: 고객이 플랫폼에 얼마나 자주 방문하고 있는지 보여주는 지표
- **인사이트**:
    - 평균 주기가 **20일 이상인 고객**은 이탈 위험이 상대적으로 높음
    - 평균 주기가 짧은 고객은 **루틴하게 사용하는 충성 고객 가능성**
""")

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.histplot(user_pattern['avg_order_interval'], bins=30, kde=True, color='skyblue', ax=ax1)
plt.axvline(x=20, color='red', linestyle='--', label='이탈 경계선 예시')
plt.title('고객 평균 주문 주기 분포')
plt.xlabel('평균 주문 주기 (일)')
plt.ylabel('고객 수')
plt.legend()
plt.grid(True)
st.pyplot(fig1)

# --- 2단계: 평균 주문 수 분석 ---
st.header("2. 평균 주문 수 분석 → 충성도, LTV 추정")

st.markdown("""
- **의미**: 고객이 플랫폼에서 얼마나 자주, 많이 주문했는지를 보여주는 지표
- **인사이트**:
    - 평균보다 많이 주문한 고객은 충성도가 높고 VIP로 볼 수 있음
    - 주문 수가 적은 고객은 신규/이탈 위험 가능성
""")

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.histplot(user_pattern['total_orders'], bins=30, color='mediumseagreen', ax=ax2)
plt.axvline(user_pattern['total_orders'].mean(), color='red', linestyle='--', label=f"평균 주문 수: {user_pattern['total_orders'].mean():.2f}")
plt.yscale('log')
plt.title('고객 총 주문 수 분포 (Log Scale)')
plt.xlabel('총 주문 수')
plt.ylabel('고객 수 (로그)')
plt.legend()
plt.grid(True)
st.pyplot(fig2)

# --- 3단계: 재주문 비율 분석 ---
st.header("3. 전체 재주문 비율 분석 → 반복구매 성향, 제품 만족도")

st.markdown("""
- **의미**: 고객이 같은 제품을 반복 구매하는 경향성 (충성도 높은 고객 확인 가능)
- **인사이트**:
    - 재주문 비율이 0.7 이상이면 제품/플랫폼에 대한 만족도가 높음
    - 0.4 이하면 충성도 낮음 또는 일회성 이용 가능성
""")

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.kdeplot(user_pattern['reorder_ratio'], fill=True, color='orange', ax=ax3)
plt.axvline(user_pattern['reorder_ratio'].mean(), color='red', linestyle='--', label='전체 평균')
plt.title('고객 재주문 비율 분포')
plt.xlabel('재주문 비율')
plt.ylabel('밀도')
plt.legend()
plt.grid(True)
st.pyplot(fig3)

# --- 4. 주문 수 vs 재주문 비율 산점도 ---
st.header("4. 고객 유형 관계 시각화")

fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=user_pattern, x='total_orders', y='reorder_ratio', alpha=0.5, ax=ax4)
plt.axvline(20, color='red', linestyle='--', label='충성 고객 기준 (20회 이상)')
plt.axhline(0.7, color='orange', linestyle='--', label='재주문율 기준 (70% 이상)')
plt.title('총 주문 수 vs 재주문 비율')
plt.xlabel('총 주문 수')
plt.ylabel('재주문 비율')
plt.legend()
plt.grid(True)
st.pyplot(fig4)

# --- 5. 충성도 세그먼트 분류 시각화 ---
st.header("5. 고객 충성도 세그먼트 분포")

def classify_customer(row):
    if row['total_orders'] >= 20 and row['reorder_ratio'] >= 0.7:
        return 'VIP 충성 고객'
    elif row['total_orders'] >= 10 and row['reorder_ratio'] >= 0.5:
        return '일반 충성 고객'
    elif row['total_orders'] < 10 and row['reorder_ratio'] < 0.4:
        return '이탈 위험군'
    else:
        return '기타'

user_pattern['loyalty_segment'] = user_pattern.apply(classify_customer, axis=1)

fig5, ax5 = plt.subplots()
user_pattern['loyalty_segment'].value_counts().plot(kind='bar', color='cornflowerblue', ax=ax5)
plt.title('고객 충성도 세그먼트 분포')
plt.ylabel('고객 수')
plt.xticks(rotation=0)
plt.grid(True)
st.pyplot(fig5)

# --- 6. 충성도별 평균 지표 비교 ---
st.header("6. 충성도 등급별 평균 지표 비교")

avg_metrics = user_pattern.groupby('loyalty_segment')[['avg_order_interval', 'total_orders', 'reorder_ratio']].mean().round(2)
st.dataframe(avg_metrics)

# --- 인사이트 요약 ---
st.header("7. 인사이트 요약")
st.markdown("""
- **이탈 위험군 특징**:
    - 평균 주문 주기: 20일 이상
    - 총 주문 수: 10회 미만
    - 재주문 비율: 0.4 이하
- **VIP 충성 고객 특징**:
    - 총 주문 수: 20회 이상
    - 재주문 비율: 0.7 이상
- **활용 방안**:
    - 이탈 위험군 → 리마인드 푸시, 할인 쿠폰 발송
    - 충성 고객 → 멤버십 전환, 추천 보상 제공
    - 신규 고객 → 온보딩 메시지 제공
""")
