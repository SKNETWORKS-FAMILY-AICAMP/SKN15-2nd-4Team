import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import joblib
import numpy as np
from PIL import Image


def model_explain():
    st.subheader("1️⃣-ⓑ 이탈 정의 📝")
    st.markdown("""
    - 이 프로젝트에서는 **고객 특성별 특정일 이상 미구매**한 고객을 **이탈 위험 고객**으로 정의
    - 마지막 주문 후 경과일(`days_since_prior_order`)을 기준으로 미구매한 고객을 이탈 위험 고객으로 간주
    - 또한, 마지막 주문 이후 구매 주기를 고려하여 평균 이상으로 **비활성 상태**인 고객도 포함
    - 데이터의 한계 : 이탈 기준일은 명확하게 이탈한 것을 판단하는 것이 아니라, **이탈했을 가능성**을 가정
        * `days_since_prior_order`(마지막 주문 후 경과일)은 데이터셋에서 최대 30일의 값을 가짐.
        * 30일 째의 이탈율은 약 30.64%로, 그 이후의 추이는 확인할 수 없음
    """)

def plot_churn_rate():
    #st.title("🧠 고객 이탈 예측 모델 설명")
    st.subheader("1️⃣ 이탈 고객 정의 기준")
    st.subheader("이탈 데이터의 특성 📊")
    st.markdown("""
    - **온라인 식료품 배달(e-grocery) 플랫폼** 실제 구매 데이터로 약 33만건
    - 예상 서비스 대상자
        * 마케팅 담당자 : 
            + 이탈 위험군 타겟 마케팅 : 이탈 위험군에 대한 리마인드, 할인 쿠폰 지급
        * 상품 기획 및 운영팀 : 
            + 상품 구성 최적화 : 이탈 고객이 많이 발생한 상품 및 카테고리를 개선
        * CRM 및 고객지원팀 :
            + 고객 이탈원인 분석 : 이탈한 고객이 마지막으로 구매한 상품 및 고객 불만 파악
        * 데이터 분석팀 :
            + 고객 행동패턴 연구 : 재구매율과 장바구니에 담은 순서를 분석 → 상품 연쇄 구매 유도
        
    """)

def set_churn():
    st.subheader("이탈 기준일 설정 ")
    
    st.write(" 1) 경과일 별 이탈율 추이")
    img = Image.open("images/churn_rate.png")
    st.image(img, caption="경과일 기준 이탈율 변화")
    st.write(" → 가설 : 기울기가 완만해지는 변곡점이 있을 것이고 기준일이 될 것이다.")

    st.write(" 2) 이탈율의 기울기와 변화율")
    img = Image.open("images/gradient.png")
    st.image(img, caption="경과일 기준 이탈율 기울기")
    img = Image.open("images/change.png")
    st.image(img, caption="경과일 기준 이탈율 변화율")
    st.markdown("""
    **→ 해석 : 식료품, 생필품 등 정기적 소비를 하는 고객이 이탈했을 것이다.** 
    **식료품 리테일 데이터에서 흔하게 관찰되는 특징과 유사함**
    **solution) 주기마다 이탈이 예상되는 시기를 예측해서 재구매를 유도하는 이벤트를 할 수 있음**
    """)

    st.write(" 3) 고객 특성별 맞춤 기준일 설정  ")
    st.write("- 정기 구매 패턴을 띄는 고객과 그렇지 않은 고객에게 다른 기준 부여")
    
    st.write(" 4) 마지막 구매 주기가 길어진 경우를 기준일로 설정  ")
    st.write("- 각 고객별 평균 구매 주기 대비, 마지막 구매 주기가 길어진 경우")
    st.write("- 위 조건에서 평소 대비 다른 요일 혹은 시각에 마지막 구매를 한 경우")

    st.write(" 5) 도메인 관행에 따른 이탈 기준일 설정  ")
    st.write("- 일반적으로 식료품 리테일 산업에서 이탈 기준일은 28일 혹은 30일로 설정")
    st.write("- 예: 쿠팡, 이마트몰, Amazon Fresh 등도 28~30일 기준 이탈률 관리")



def analyze_regular_customer_churn():
    import streamlit as st
    import pandas as pd

    st.subheader("정기 구매 고객의 패턴 이탈 분석")
    st.markdown("""
    - 정기적으로 반복 구매하는 고객군(예: 식료품, 생필품 등)의 이탈 패턴을 별도로 분석합니다.
    - 구매 주기가 일정한 고객은 패턴 변화, 스케줄 변경으로 이탈 신호를 포착합니다.
    - 고객 유형별로 이탈 기준을 다르게 적용합니다.
    """)
    # 예시 데이터 요약
    st.markdown("**정기구매 고객 이탈 패턴 분석 결과 요약**")
    st.markdown("- 전체 정기구매 고객 수: 9,660명")
    st.markdown("- 패턴 이탈 위험 정기구매 고객 수: 924명")
    st.markdown("- 예시 고객ID 5개: 13, 1322, 1567, 1691, 1855")

    # 표 형태로 데이터 예시 출력 (한글 컬럼, 인덱스 제거)
    example_data = [
        [13, 1, 1, 0],
        [1322, 1, 0, 1],
        [1567, 1, 1, 1],
        [1691, 1, 0, 0],
        [1855, 1, 1, 0],
    ]
    columns = ['고객ID', '정기 구매 여부', '패턴 이탈 여부', '스케줄 변경 여부']
    df_example = pd.DataFrame(example_data, columns=columns)
    df_example.index = [''] * len(df_example)
    st.markdown("**정기구매 고객 분석 결과 (예시)**")
    st.table(df_example)

    # 통계 요약 표 (인덱스 제거)
    summary_data = {
        '전체 고객 수': [20629],
        '정기구매 고객 수': [9660],
        '패턴 이탈 고객 수': [1090],
        '스케줄 변화 고객 수': [924]
    }
    df_summary = pd.DataFrame(summary_data)
    df_summary.index = ['']
    st.markdown("**정기구매 고객 분석 통계**")
    st.table(df_summary)
    

    



def analyze_churn_by_order_cycle():
    st.subheader("평균 주문 주기를 초과한 고객 이탈 분석 ⏳")
    st.markdown("##### 1) 기준별 이탈률 변화")

    # 배수와 이탈률 데이터
    multiples = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
    churn_rates = [46.34, 39.10, 32.87, 27.14, 22.31, 18.73, 15.63, 12.97, 10.88, 8.99, 7.61, 6.40, 5.44, 4.55, 3.84]

    # 배수 값을 "1.1배" 형식으로 변환
    multiples_str = [f"{m:.1f}배" for m in multiples]

    # 데이터프레임 생성
    df = pd.DataFrame({
        '평균 주문 주기 배수': multiples_str,
        '이탈률 (%)': churn_rates
    })

    # 인덱스 제거 후 표 출력
    df.index = [''] * len(df)
    st.table(df)

    # 실제 환경에서는 아래 코드의 주석을 해제하여 이미지 사용
    # from PIL import Image
    # img = Image.open("churn_by_cycle.png")
    # st.image(img, caption="평균 주문 주기 배수별 이탈률 변화")

    st.write(" 2) 이탈 위험 주기 상수별 이탈율(m : 위험 주기=평균주기*m)")
    img = Image.open("images/average_churn.png")
    st.image(img, caption="위험주기 상수에 따른 이탈율")


    
    


