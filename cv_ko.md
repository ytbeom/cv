# 유택범

- 직함: Software Engineer
- 전화: 010-6481-8603
- 이메일: ytbeom@gmail.com
- LinkedIn: taekbeomyoo

생성형 AI 검색 서비스의 Backend를 개발하는 Software Engineer입니다. LLM·Agent 기반 서비스를 실제 트래픽 환경에서 안정적으로 설계하고 운영하며, AI 기술을 확장 가능한 제품으로 구현하는 데 관심이 있습니다.

## 경력

### NAVER

- 기간: 2021.04 - 현재
- 직책: Software Engineer

#### AI 탭

- 기간: 2026.03 - 현재
- 기술: Python, FastAPI

* 검색 의도와 맥락을 이해해 대화형 정보 탐색을 제공하는 생성형 AI 검색 서비스
* LangGraph 기반 AI Agent를 실행하고 SSE로 실시간 응답을 제공하는 AI Serving Backend를 설계·개발·운영
* Streaming chunk 경계를 고려한 공통 Parser를 구현하고, hold buffer + Aho-Corasick 기반 금칙어 탐지와 LLM 구조화 출력의 Frontend 이벤트 변환에 활용
* Reasoning 구간의 이벤트 부족으로 SSE disconnect 감지가 지연되는 문제를 해결하기 위해 0.5초 heartbeat를 도입하여 평균 1.5초 이내 연결 종료를 감지하고 응답 중단 지표의 정확도를 개선
* 100 Pod 규모에서 평균 30QPS(최대 50QPS)를 처리하는 서비스를 운영하고, Grafana·Prometheus 기반 latency, error, timeout, disconnect 지표를 설계

#### AI 브리핑

- 기간: 2025.04 - 2026.02
- 기술: Python, FastAPI, LangGraph, Kafka

* 검색 결과를 생성형 AI로 요약해 핵심 정보와 출처, 관련 질문을 제공하는 AI 검색 서비스
* LangGraph 기반 생성 Workflow를 설계하고 실시간 생성 API와 Batch 생성 Pipeline을 공통 Backend로 개발·운영
* Kafka 기반 Batch 생성 Pipeline을 구축하고 Topic별 우선순위를 적용하여 GPU 자원을 효율적으로 활용
* 검색 결과만으로 정보가 부족한 질의를 대상으로 Iterative Retrieval Workflow를 구현하고, LLM이 부족한 정보를 분석해 추가 검색 Keyword를 생성하도록 설계
* LLM-as-a-Judge 기반 평가 Prompt를 설계하고 자동 평가 환경을 구축하여 Iterative Retrieval Workflow의 품질을 검증
* 120B Teacher Model로 생성한 Dataset을 활용해 3B Model SFT를 수행하고 품질 및 추론 비용 개선 가능성을 검증

#### 동영상 검색 데이터 정제

- 기간: 2023.07 - 2024.12
- 기술: Scala, Spark, Python, React

* 다양한 출처의 동영상 데이터를 검색 색인용 공통 스키마로 정규화하는 대규모 ETL Pipeline
* 약 10억 건 규모의 동영상 검색 색인 데이터를 생성하는 Scala Spark 기반 ETL Pipeline을 유지보수하고 신규 출처 연동 및 검색 품질 개선 기능을 개발
* Weverse 등 신규 동영상 출처를 연동하고 출처별 메타데이터 및 색인 정책을 반영
* YouTube Chapter 정보를 색인 데이터에 추가하여 주요 장면 이동을 지원하고, 검색 품질 평가 도구를 개발하여 자사·경쟁사 검색 결과의 적절성 및 시의성을 비교 평가할 수 있는 환경 구축

#### Key Moments

- 기간: 2022.09 - 2024.12
- 기술: Python, Kafka, Airflow

* AI 기반으로 동영상 내 주요 장면을 자동 탐지하고 검색 결과에서 해당 시점으로 바로 이동할 수 있는 정보를 제공하는 서비스
* Action Recognition과 OCR 결과를 결합하여 골프 영상에서 "선수명 + 동작" 형태의 검색 가능한 Key Moment를 생성하는 로직을 설계
* 기존 영상 처리 Pipeline을 확장하여 Airflow → Kafka → Consumer → Redis 기반으로 Action Recognition 결과를 처리하고, 이를 골프 도메인의 Key Moment 생성에 활용
* 생성된 Key Moment를 네이버 동영상 검색 결과에 연동하여 주요 장면의 제목·썸네일·타임스탬프를 제공

#### Dynamic Product Ads

- 기간: 2021.12 - 2022.08
- 기술: Kotlin, Spring Boot, Kafka, Redis, MongoDB, Kubernetes, React

* 사용자의 상품 탐색 이력을 기반으로 개인화된 상품 광고를 노출하는 성과형 광고 상품
* 실시간 광고 Serving Server와 사용자 행동 데이터 처리 Pipeline을 개발·운영하고, 사용자·상품 단위 노출 제한 및 스토어 관심 신호 기반 타게팅 기능을 개발
* 렌더링 모듈을 별도 컨테이너로 분리하고 Kubernetes health check 범위를 조정하여 렌더링 장애의 전파를 방지
* 기획·QA 조직이 광고 응답 및 지면별 노출 가능 상품을 직접 확인할 수 있는 운영 도구를 개발

#### LINE Chirashi

- 기간: 2021.04 - 2022.01
- 기술: Java, Spring, MongoDB, Redis

* 오프라인 매장의 전단 정보를 디지털화하고 사용자 관심·방문 이력을 기반으로 개인화된 광고를 제공하는 서비스
* 대용량 사용자 데이터를 기반으로 관심 매장·최근 방문·주변 매장 기준 광고 타게팅 대상을 추출하는 배치 Pipeline을 개발·운영
* 캐싱 증가로 발생한 JVM 메모리 부족 장애를 heap 및 캐싱 구조 개선으로 해결

### Tmax

- 기간: 2019.02 - 2021.04
- 직책: Software Engineer

* Java 기반 Enterprise 서비스 Backend 및 React 기반 Frontend 개발, REST API 개발, Database 설계
* 5인 규모 개발팀 리드

## 학력

### 서울대학교

- 기간: 2015.09 – 2022.02
- 직책: 산업공학 석사

* 서울, 대한민국

### POSTECH

- 기간: 2010.03 – 2015.02
- 직책: 산업경영공학 / 컴퓨터공학 학사 (복수전공)

* 포항, 대한민국

## 연구 경험

### 서울대학교 삶향상기술연구실

- 직책: 석박사통합과정

* 인간공학(Human Factors) 기반의 사용자 행동 분석 및 사용자 중심 인터페이스·시스템 설계 연구 수행

#### 주요 논문

* Mode Displaying Mouse Cursors for Reducing Input Language Mode Confusion: Utility and User Attitude Evaluation - 제1저자, Applied Ergonomics, 2021
* A Reach Motion Generation Algorithm Based on Posture Memories - 제1저자, WORK, 2020
* An Explorative Study on Crossmodal Congruence Between Visual and Tactile Icons Based on Emotional Responses - 제1저자, ACM ICMI, 2014
