# WeatherFit AI

오늘의 실제 날씨와 사용자의 스타일 정보를 함께 고려하여
개인 맞춤형 코디를 추천해주는 AI 웹 서비스입니다.

사용자는 지역, 체형, 퍼스널 컬러, 키, 원하는 스타일,
오늘의 일정과 추가 요청을 입력할 수 있습니다.

WeatherFit AI는 실제 날씨 정보를 불러온 뒤
해당 정보를 사용자 입력과 함께 AI에 전달하여
맞춤형 코디를 텍스트로 추천합니다.

추천된 코디는 AI 이미지 생성 기능을 통해
시각적인 코디 이미지로도 확인할 수 있습니다.


## 주요 기능

- 지역별 실제 날씨 정보 조회
- 현재 기온, 체감 온도, 최고·최저 기온, 강수 확률 확인
- 체형 및 퍼스널 컬러 입력
- 키와 스타일 선호사항 입력
- 일정과 원하는 스타일에 따른 AI 코디 추천
- AI 추천 코디 이미지 생성
- 모바일 및 데스크톱 반응형 화면
- 입력 오류 및 API 오류 안내


## 페이지 구성

### HOME
서비스 소개와 오늘의 날씨를 확인할 수 있습니다.

### MY STYLE
사용자의 체형, 퍼스널 컬러, 키와 코디 선호사항을 입력할 수 있습니다.

### OUTFIT
오늘의 일정과 원하는 스타일을 선택하고,
AI 맞춤 코디 추천을 받을 수 있습니다.

### ABOUT
WeatherFit AI 서비스의 목적과 주요 기능을 소개합니다.


## AI 기능

### 입력

AI 코디 추천에는 다음 정보가 사용됩니다.

- 실제 날씨 정보
- 지역
- 체형
- 퍼스널 컬러
- 키
- 코디 선호사항
- 오늘의 일정
- 원하는 스타일
- 추가 요청

### 출력

AI는 다음과 같은 내용을 포함한 코디를 추천합니다.

- 상의
- 하의
- 아우터
- 신발
- 추천 색 조합
- 날씨를 고려한 이유
- 스타일을 고려한 이유

추천 결과를 기반으로 AI 코디 이미지도 생성할 수 있습니다.


## 기술 스택

### Frontend

- HTML
- CSS
- Vanilla JavaScript

### Backend

- Python
- Vercel Serverless Functions

### API

- Open-Meteo API
  - 실제 날씨 정보 조회
- Codyssey Public API
  - AI 코디 텍스트 생성
  - AI 코디 이미지 생성

### Deployment

- GitHub
- Vercel


## 프로젝트 구조

```text
weatherfit-ai/
│
├── api/
│   ├── outfit.py
│   └── outfit-image.py
│
├── css/
│   └── style.css
│
├── js/
│   └── main.js
│
├── Screenshot/
│
├── index.html
├── dev_server.py
├── requirements.txt
├── pyproject.toml
├── vercel.json
├── .gitignore
└── README.md