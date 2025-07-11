import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import joblib
import numpy as np
from utils.streamlit_variable_rank_by_importance import feature_importance_df, train_variable

def model_explain():
    st.title("🧠 고객 이탈 예측 모델 설명")

    # ---------------------
    # 1. 이탈 정의
    # ---------------------
    st.header("1️⃣ 이탈 고객 정의 기준")
    st.markdown("""
    - 이 프로젝트에서는 **'30일 이상 미구매'**한 고객을 **이탈 고객**으로 정의했습니다.
    - 또한, 마지막 주문 이후 구매 주기를 고려하여 평균 이상으로 **비활성 상태**인 고객도 포함했습니다.
    """)

    # ---------------------
    # 2. 사용한 변수
    # ---------------------
    st.header("2️⃣ 사용된 주요 변수 (Feature)")
    train_variable()
    
    # ---------------------
    # 3. 모델 성능
    # ---------------------
    st.header("3️⃣ 예측 모델 및 성능")
    model_info = {
        "모델": "LightGBM (Binary Classifier)",
        "AUC Score": "0.87",
        "정확도": "82%",
        "정밀도 (Precision)": "75%",
        "재현율 (Recall)": "68%",
        "F1 Score": "71%"
    }
    st.table(pd.DataFrame(model_info.items(), columns=["항목", "값"]))

    # ---------------------
    # 4. 중요 변수 시각화
    # ---------------------
    st.header("4️⃣ 변수 중요도 분석")
    
    st.subheader('상관 관계 히트맵 분석')
    st.image("../images/heatmap.png",caption="변수 중요도 분석 (shap)", use_container_width=True)
    st.markdown("""
                - 이탈 예측에 마지막 주문 간격 (last_cycle)과 평균 구매 주기(avg_cycle), 이탈 기준 주기(churn_risk_cycle)이 가장 높은 중요도을 보임
                - 즉, 주기적으로 오래 쉬었다가 구매하는 패턴일수록 이탈 위험이 크다는 것을 의미함.
                """)
    
    feature_importance_df()
    st.markdown("""
                - 상관 관계 히트맵 기반의 상위 10개의 변수 중요도를 나타냄
                """)
    
    st.subheader('')
    st.image("../images/Decisiontree.png",caption="결정 트리 시각화", use_container_width=True)
    st.markdown("""
                - 이전 주문 이후 경과 시간(hours_since_prior_order)을 통해 최근에 구매 안 한 고객이냐에 따라 이탈 여부를 크게 나눔
                - 왼쪽 가지를 통해 비교적 최근에 구매한 사용자인 경우 추가로 churn_risk_cycle, last_cycle, dow_hour_outlier 등으로 분기 됨을 알 수 있음
                - 오른쪽 가지를 통해 구매 간격이 긴 사용자인 경우 추가로 churn_risk_cycle, age_cycle, order 시간대 패턴 등을 통해 이탈 여부를 판단함
                """)
    
    st.subheader('SHAP 기반의 변수 중요도 분석')
    st.image("../images/shap.png",caption="변수 중요도 분석 (shap)", use_container_width=True)
    st.markdown("""
                - 모델이 예측을 내릴 때 각 feature가 얼마나 영향을 미쳤는지 SHAP 값 기준으로 시각화
                - 위에서부터 중요도가 높은 feautre로 최근 구매 주기 (last_cycle), 이전 주문으로부터 경과일 (days_since_prior_order), 이전 주문으로부터 경과 시간 (hours_since_prior_order), 평균 구매 간격 (avg_cycle), 이탈 위험도 계산 기반 (churn_risk_cycle) 순으로 낮아짐.
                - 빨간색은 해당 feature 값이 크다는 것을 의미하고 파란색은 해당 feature 값이 작다는 것을 의미함
                - last_cycle이 높을수록 이탈 예측에 기여함.
                - 구매 주기/간격이 길수록 이탈로 예측되는 경향을 보임
                """)

    # # 저장된 모델과 SHAP 값 불러오기
    # try:
    #     model = joblib.load("models/lgbm_model.pkl")
    #     X_sample = pd.read_csv("data/X_sample.csv")  # 훈련셋 샘플 (100개 정도)
    #     explainer = shap.TreeExplainer(model)
    #     shap_values = explainer.shap_values(X_sample)

    #     st.subheader("🎯 주요 변수별 영향 (SHAP Summary Plot)")
    #     fig, ax = plt.subplots()
    #     shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
    #     st.pyplot(fig)

    # except Exception as e:
    #     st.warning("SHAP 그래프를 불러오지 못했습니다. SHAP 값과 샘플 데이터를 준비해 주세요.")
    #     st.code(f"{e}")
