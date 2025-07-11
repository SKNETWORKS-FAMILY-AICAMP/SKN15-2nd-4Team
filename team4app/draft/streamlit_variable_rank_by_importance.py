import streamlit as st
import pandas as pd

# 변수 중요도 딕셔너리
importance_dict = {
    'last_cycle': 0.409005,
    'avg_cycle': 0.080339,
    'churn_risk_cycle': 0.073583,
    'order_number': 0.060914,
    'hours_since_first_order': 0.059019,
    'user_id': 0.057769,
    'days_since_first_order': 0.056678,
    'hours_since_prior_order': 0.047953,
    'order_hour_of_day': 0.042336,
    'prev_hour': 0.040231,
    'days_since_prior_order': 0.033562,
    'order_dow': 0.031431,
    'regular_pattern': 0.003425,
    'dow_hour_outlier': 0.001987,
    'out_of_pattern': 0.001769
}

# 한글 설명 매핑
name_mapping = {
    'user_id': '유저 번호',
    'order_number': '유저별 주문 횟수',
    'days_since_prior_order': '이전 주문 이후 경과 일수',
    'days_since_first_order': '첫 주문 이후 경과 일수',
    'order_hour_of_day': '주문 시간',
    'prev_hour': '이전 주문 시간',
    'hours_since_prior_order': '이전 주문 이후 경과 시간',
    'hours_since_first_order': '첫 주문 이후 경과 시간',
    'order_dow': '주문 요일',
    'regular_pattern': '정기구매 패턴 여부',
    'out_of_pattern': '패턴 벗어남 여부',
    'dow_hour_outlier': '요일/시간대 이탈 여부',
    'avg_cycle': '평균 구매 주기',
    'last_cycle': '마지막 주문 간격',
    'churn_risk_cycle': '이탈 기준 주기'
}

# 데이터프레임 생성 및 정렬
df = pd.DataFrame(list(importance_dict.items()), columns=['영문 변수명', '중요도'])
df['한글 설명'] = df['영문 변수명'].map(name_mapping)
df = df[['영문 변수명', '한글 설명', '중요도']]
df = df.sort_values(by='중요도', ascending=False).head(10).reset_index(drop=True)
df.insert(0, '순위', [(f"{i+1}순위") for i in range(len(df))])

# 제목
st.title("상위 10개 변수 중요도")

# 테이블을 HTML로 변환하여 인덱스 없이 출력
st.markdown(df.to_html(index=False), unsafe_allow_html=True)
