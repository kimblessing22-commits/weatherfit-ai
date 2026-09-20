# WeatherFit AI

## Live Demo

- **배포된 웹 서비스:** [https://weatherfit-ai.vercel.app](https://weatherfit-ai.vercel.app)
- **GitHub 저장소:** [https://github.com/kimblessing22-commits/weatherfit-ai](https://github.com/kimblessing22-commits/weatherfit-ai)

본 서비스는 Vercel Production 환경에 배포되어 있으며,
위 배포 URL에서 실제 날씨 조회, AI 코디 추천, AI 코디 이미지 생성 기능을 직접 테스트할 수 있습니다.

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

## 배포 오류 진단 및 재배포 절차

배포된 서비스에서 오류가 발생하면 다음 순서로 문제를 확인한다.

1. 브라우저 개발자 도구의 `Network` 탭에서 실패한 API 요청을 확인한다.
2. 요청의 상태 코드(예: 400, 500)와 `Response` 내용을 확인하여 오류 원인을 파악한다.
3. Vercel 프로젝트의 Environment Variables에서 필요한 환경 변수가 올바르게 설정되어 있는지 확인한다.
4. 필요하면 Vercel의 배포 로그를 확인하여 Python Serverless Function의 실행 오류를 확인한다.
5. 코드 또는 환경 변수를 수정한 뒤 GitHub에 변경사항을 push하거나 Vercel Production 배포를 다시 수행한다.
6. 배포 완료 후 실제 Production URL에서 다시 전체 기능을 테스트한다.

실제 개발 과정에서도 `/api/outfit` 요청에서
`500 Internal Server Error`가 발생한 적이 있었다.

Chrome DevTools의 Network 탭에서 Response를 확인한 결과
`CODYSSEY_API_KEY가 설정되지 않았습니다.`라는 오류를 확인하였다.

이후 Vercel Production 환경 변수 설정을 확인하고
Production 재배포를 수행하여 문제를 해결하였다.

## API 키 유출 사고 대응 절차

API 키가 외부에 노출되었거나 유출이 의심되는 경우 다음 순서로 대응한다.

1. 노출된 기존 API 키를 즉시 폐기한다.
2. 새로운 API 키를 발급한다.
3. Vercel Environment Variables의 `CODYSSEY_API_KEY` 값을 새 키로 교체한다.
4. 로컬 `.env` 파일의 키도 새 값으로 변경한다.
5. GitHub 커밋 이력과 로그에서 키가 노출되었는지 확인한다.
6. 키가 Git 기록에 포함된 경우 해당 커밋 이력을 정리하고 다시 push한다.
7. Vercel Production을 다시 배포한다.
8. 새 키로 AI 기능이 정상 작동하는지 다시 테스트한다.

API 키는 코드나 README에 직접 작성하지 않으며,
`.env` 파일은 `.gitignore`를 통해 GitHub에 업로드되지 않도록 관리한다.

## 성능 및 운영 개선 방향

현재 WeatherFit AI는 사용자가 요청할 때마다 외부 AI API를 실시간으로 호출하는 구조이다.

향후 사용자가 많아질 경우 다음과 같은 방식으로 성능과 운영 효율을 개선할 수 있다.

1. 동일하거나 반복되는 요청 결과를 일정 시간 캐싱한다.
2. 사용자가 버튼을 여러 번 연속으로 누르는 중복 요청을 방지한다.
3. 사용자별 요청 횟수를 제한하여 과도한 API 호출을 줄인다.
4. 이미지 생성처럼 처리 시간이 긴 작업은 비동기 처리 또는 별도 작업 흐름으로 분리하는 방안을 고려한다.
5. 텍스트 추천과 이미지 생성을 분리하여 필요한 기능만 호출하도록 유지한다.

캐싱은 응답 속도와 API 비용을 줄이는 데 도움이 되지만,
날씨 정보처럼 자주 바뀌는 데이터는 너무 오래 캐싱하면 최신성이 떨어질 수 있다.

따라서 실제 운영 환경에서는 데이터 종류에 따라 적절한 캐시 만료 시간을 설정하고,
속도·비용·최신성 사이의 균형을 고려해야 한다.

## 프레임워크 도입 시 고려사항

현재 WeatherFit AI는 과제 요구사항에 따라
Vanilla HTML, CSS, JavaScript로 구현하였다.

현재 규모에서는 별도의 프레임워크 없이도
화면 구성, 사용자 입력 처리, API 호출, 결과 표시를 충분히 구현할 수 있기 때문에
구조를 단순하게 유지할 수 있다는 장점이 있다.

향후 서비스 규모가 커져 화면과 기능이 많아질 경우
React 또는 Vue와 같은 프레임워크 도입을 고려할 수 있다.

프레임워크를 도입할 경우의 장점은 다음과 같다.

- 화면을 컴포넌트 단위로 분리하여 관리하기 쉬워진다.
- 사용자 입력과 결과 상태를 체계적으로 관리할 수 있다.
- 반복되는 UI를 재사용하기 쉬워진다.
- 기능이 많아질수록 유지보수가 편리해질 수 있다.

반면 다음과 같은 비용도 발생한다.

- 빌드 환경과 패키지 의존성이 추가된다.
- 프로젝트 구조가 현재보다 복잡해진다.
- 간단한 서비스에서는 오히려 학습 및 관리 비용이 커질 수 있다.

향후 React 또는 Vue로 전환할 경우에는 다음과 같이 단계적으로 마이그레이션할 수 있다.

1. HOME, MY STYLE, OUTFIT, ABOUT 섹션을 각각 컴포넌트로 분리한다.
2. 현재 `main.js`에서 처리하는 사용자 입력값과 화면 상태를 컴포넌트 상태로 이동한다.
3. 날씨 조회와 AI 요청 로직을 별도의 함수 또는 서비스 모듈로 분리한다.
4. 기존 Python Serverless Functions인 `/api/outfit`과 `/api/outfit-image`는 그대로 유지한다.
5. 프론트엔드와 백엔드 사이의 JSON 요청/응답 형식은 가능하면 동일하게 유지하여 변경 범위를 줄인다.