# WeatherFit AI 실행 및 배포 증빙

## 1. 프로젝트 저장소

GitHub Repository:

https://github.com/kimblessing22-commits/weatherfit-ai

프로젝트에는 다음 구조가 포함되어 있다.

- `index.html`
- `css/style.css`
- `js/main.js`
- `api/outfit.py`
- `api/outfit-image.py`
- `README.md`
- `SERVICE_PLAN.md`
- `TEST_RESULTS.md`

프론트엔드와 Python Serverless Functions를 분리하여 구성하였다.


## 2. Production 배포 URL

WeatherFit AI는 Vercel Production 환경에 배포하였다.

Production URL:

https://weatherfit-ai.vercel.app

실제 배포 URL에서 다음 기능의 정상 작동을 확인하였다.

- 페이지 및 섹션 네비게이션
- 실제 날씨 데이터 조회
- 사용자 스타일 정보 입력
- AI 텍스트 코디 추천
- AI 코디 이미지 생성
- 모바일 반응형 화면


## 3. 배포 과정

GitHub 저장소와 Vercel 프로젝트를 연결하여 배포하였다.

Production 재배포가 필요한 경우 다음 명령을 사용하였다.

```bash
vercel deploy --prod
실제 개발 과정에서 환경 변수 설정 문제로
/api/outfit 요청이 HTTP 500 오류를 반환한 적이 있었다.

Chrome DevTools의 Network 탭에서 Response를 확인하여

CODYSSEY_API_KEY가 설정되지 않았습니다.

라는 원인을 확인하였다.

이후 Vercel Production 환경 변수 설정을 확인하고
Production을 다시 배포하였다.

재배포 후 AI 텍스트 추천 및 이미지 생성 기능이 모두 정상 동작하였다.

4. Git 변경 이력

프로젝트 개발 과정에서는 Git을 통해 변경사항을 기록하였다.

주요 작업 내용:

초기 WeatherFit AI 프로젝트 생성
프론트엔드 HTML/CSS/JavaScript 구현
Python Serverless Functions 구현
Codyssey AI API 연동
이미지 생성 API 연동
반응형 UI 적용
README 및 서비스 기획서 작성
실행 및 AI 활용 증빙 추가
서버 측 입력 검증 보완

변경사항은 git add, git commit, git push 과정을 통해
GitHub 저장소에 반영하였다.

5. 스크린샷 증빙

실제 서비스 실행 화면 및 AI 코딩 도구 활용 과정의 이미지는
프로젝트의 Screenshot/ 폴더에 저장하였다.

해당 폴더에는 다음과 같은 증빙이 포함되어 있다.

데스크톱 실행 화면
모바일 반응형 화면
AI 텍스트 추천 결과
AI 코디 이미지 생성 결과
AI를 활용한 코드 구현 과정
JavaScript 및 배포 오류 디버깅 과정
Codyssey API 연동 과정

AI 사전평가에서는 PNG 이미지 내용이 직접 평가되지 않을 수 있으므로,
스크린샷으로 확인한 주요 실행 결과와 문제 해결 과정은
TEST_RESULTS.md와 본 문서에도 텍스트로 기록하였다.

6. 최종 동작 확인

최종 Production 환경에서 아래 순서로 전체 기능을 검증하였다.

지역 선택
날씨 정보 조회
체형, 퍼스널 컬러, 키 및 스타일 정보 입력
일정과 원하는 스타일 선택
AI 코디 추천 요청
AI 텍스트 코디 결과 확인
AI 코디 이미지 생성
모바일 화면에서 반응형 레이아웃 확인

최종 결과: PASS