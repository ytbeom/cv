# 유택범

- 직함: Software Engineer
- 전화: 010-6481-8603
- 이메일: ytbeom@gmail.com
- LinkedIn: taekbeomyoo

생성형 AI 검색 서비스의 backend를 개발하는 Software Engineer입니다. LLM·agent 기반 서비스를 실제 트래픽 환경에서 안정적으로 설계하고 운영하며, AI 기술을 확장 가능한 제품으로 구현하는 데 관심이 있습니다.

## 경력

### NAVER

- 로고: naver.png
- 기간: 2021.04 - 현재
- 직책: Software Engineer

#### AI 탭

- 기간: 2026.03 - 현재
- 기술: Python, FastAPI

* 대화형 AI 검색 서비스의 serving backend를 신규 설계·개발
* 질의 분석, 검색 결과 수집, 멀티턴 context 조회 등 전처리부터 LangGraph 기반 AI agent 실행 및 SSE streaming까지 전 과정을 구현
* LangGraph·모델·gateway·frontend 등 여러 팀 시스템의 경계에서 인터페이스를 정의하고 변경 사항을 조율
* 100 pod 규모에서 평균 30 QPS(최대 50 QPS) 트래픽을 처리하며 Grafana·Prometheus 기반 운영 지표를 설계

#### AI 브리핑

- 기간: 2025.04 - 2026.02
- 기술: Python, FastAPI, LangGraph, Kafka

* 검색 결과를 AI로 요약하는 서비스의 생성 workflow를 LangGraph 기반으로 설계하고 실시간·batch 공통 backend를 개발
* Kafka 기반 batch 생성 pipeline을 구축하고 topic별 우선순위를 적용하여 GPU 자원을 효율적으로 활용
* 검색 결과만으로 정보가 부족한 질의에 대해 LLM이 추가 검색을 수행하는 workflow를 구현하고, LLM-as-a-Judge 자동 평가로 품질을 검증
* 120B teacher model 생성 dataset으로 3B model SFT를 수행하고 품질 및 비용 개선 가능성을 검증

#### 동영상 검색 데이터 정제

- 기간: 2023.07 - 2024.12
- 기술: Scala, Spark, Python, React

* 약 10억 건 규모의 동영상 검색 색인을 생성하는 Scala Spark 기반 ETL pipeline을 유지보수
* Weverse 등 신규 동영상 출처를 연동하고 출처별 메타데이터 및 색인 정책을 반영
* YouTube chapter 정보를 색인 데이터에 추가하여 주요 장면 이동을 지원하고, 검색 품질 평가 도구를 개발하여 자사·경쟁사 검색 결과를 비교 평가할 수 있는 환경 구축

#### Key Moments

- 기간: 2022.09 - 2024.12
- 기술: Python, Kafka, Airflow

* action recognition과 OCR 결과를 결합하여 골프 동영상 내 주요 장면을 자동 생성하는 로직을 설계

#### Dynamic Product Ads

- 기간: 2021.12 - 2022.08
- 기술: Kotlin, Spring Boot, Kafka, Redis, MongoDB, Kubernetes, React

* 개인화 상품 광고 서비스의 실시간 serving server와 사용자 행동 데이터 처리 pipeline을 개발하고, 사용자·상품 단위 노출 제한 및 타게팅 기능을 구현
* 기획·QA 조직이 광고 응답 및 지면별 노출 가능 상품을 직접 확인할 수 있는 운영 도구를 개발

#### LINE Chirashi

- 기간: 2021.04 - 2022.01
- 기술: Java, Spring, MongoDB, Redis

* 오프라인 매장 전단 광고 서비스의 타게팅 대상을 추출하는 batch pipeline을 개발하여 관심 매장·최근 방문·주변 매장 기준으로 광고 대상을 선별

### Tmax

- 로고: tmax.png
- 기간: 2019.02 - 2021.04
- 직책: Software Engineer

* Java 기반 enterprise 서비스 backend 및 React 기반 frontend 개발, REST API 개발, database 설계
* 5인 규모 개발팀 리드

## 학력

### 서울대학교

- 로고: snu.png
- 기간: 2015.09 - 2022.02
- 직책: 산업공학 석사 (삶향상기술연구실)

* 인간공학(Human Factors) 기반의 사용자 행동 분석 및 사용자 중심 인터페이스·시스템 설계 연구 수행

### POSTECH

- 로고: postech.png
- 기간: 2010.03 - 2015.02
- 직책: 산업경영공학 / 컴퓨터공학 학사 (복수전공)
