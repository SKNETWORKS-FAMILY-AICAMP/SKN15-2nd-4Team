# team4app 실행 방법

1. mydata 다운로드 후 경로 설정
2. 환경 설정

    * cmd 창에서 t4_app 위치로 이동
    * 가상환경생성
    `conda create -n p4 python=3.11 -y`
    * 가상환경활성화
    `conda activate p4`
    * 관련 모듈 설치
    `pip install -r requirements.txt`
    * 모듈 실행
    `streamlit run main.py`

* 아직 완성본 화면이 아니며, 추가로 모듈 설치가 필요할 수 있음.