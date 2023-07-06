** [ 데이터 분석 및 시각화 ] **
1. 호선별 총 인구 분석
   1.1 역별 시간대별 승/하차 인구 분석
        1.1.1 table / bar plot / line plot
        1.1.2 heat table
   1.2 역별 분석 결과 지도에 표시
        1.2.1 folium - heat map
2. 급행 열차 계획
    2.1 역별 유동인구수 상위권 추출
        2.1.1 table
    2.2 상위 호선 추출
    2.3 급행 정차 역 선정
    2.4 급행 열차 노선도 그리기
        2.4.1 googlemap 지도에 표시
   
- 활용 데이터
1.1 서울시 지하철 시간대별 승하차인원.csv
1.2 서울시지하철2022.05-2023.05.csv
2. 서울시지하철2022.05-2023.05.csv

  
** [ 어플리케이션 ] ** (Flask 활용)
1. 인터렉티브 맵 구축
    1.1 Marker을 이용하여 지하철 역 표기 / 팝업창에 지하철 탑승시간별
        - 현재 시간대
        - 평균 이용자 수
        - 엘리베이터 및 에스컬레이터 정보 표기
    1.2 Marker을 이용하여 근처 개방화장실 장소 표시
        1.2.1 화장실 주소 및 리뷰 수 웹크롤링
        1.2.2 화장실 리뷰 자연어 처리
2. 호선 / 시간대 입력 시 평균 이용자 수 차트 띄우기
    2.1 heat table / line plot (edited)

- 활용 데이터
1.1 서울시 지하철 주소.csv / 데이터 시각화 1.1에서 정제된 data 사용 / 엘레베이터 및 에스컬레이터 데이터 필요
1.2 화장실 주소 웹크롤링
2. 데이터 시각화 1.1에서 정제된 data 사용

  
:sparkles:️ note :sparkles:️
서울특별시 내에 있는 지하철 역으로 제한
1~9호선에 있는 지하철 역으로 제한