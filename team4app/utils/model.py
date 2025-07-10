import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import joblib
import numpy as np


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
    features = {
        "총 주문 수": "고객의 총 구매 횟수",
        "평균 주문 간격": "구매 간의 평균 일 수",
        "최근 구매일로부터 경과일": "현재까지 마지막 구매 이후 지난 일수",
        "카테고리 다양성": "고객이 구매한 서로 다른 카테고리 수",
        "재구매 비율": "전체 구매 중 재구매로 판단된 비율",
        "회원 등급": "고객의 멤버십 등급 (Basic~Platinum)"
    }
    st.dataframe(pd.DataFrame(features.items(), columns=["변수명", "설명"]))

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
    st.header("4️⃣ 변수 중요도 분석 (SHAP or Feature Importance)")

    # 저장된 모델과 SHAP 값 불러오기
    try:
        model = joblib.load("models/lgbm_model.pkl")
        X_sample = pd.read_csv("data/X_sample.csv")  # 훈련셋 샘플 (100개 정도)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)

        st.subheader("🎯 주요 변수별 영향 (SHAP Summary Plot)")
        fig, ax = plt.subplots()
        shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
        st.pyplot(fig)

    except Exception as e:
        st.warning("SHAP 그래프를 불러오지 못했습니다. SHAP 값과 샘플 데이터를 준비해 주세요.")
        st.code(f"{e}")
