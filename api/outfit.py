from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error


def generate_outfit_with_ai(data):

    api_key = os.environ.get("CODYSSEY_API_KEY")

    if not api_key:
        raise Exception(
            "CODYSSEY_API_KEY가 설정되지 않았습니다."
        )

    weather = data["weather"]
    user = data["user"]
    outfit = data["outfit"]

    prompt = f"""
너는 사용자의 상황에 맞는 실용적인 패션 코디를 제안하는 스타일 어시스턴트야.

아래 정보를 종합해서 오늘 입기 좋은 코디를 추천해줘.

[오늘의 실제 날씨]
지역: {weather["city"]}
현재 기온: {weather["currentTemperature"]}도
체감 온도: {weather["apparentTemperature"]}도
최고 기온: {weather["maxTemperature"]}도
최저 기온: {weather["minTemperature"]}도
강수 확률: {weather["precipitationProbability"]}%

[사용자 정보]
체형: {user["bodyType"]}
퍼스널 컬러: {user["personalColor"]}
키: {user["height"]}cm
원하는 점: {", ".join(user["preferences"])}

[오늘의 상황]
일정: {outfit["occasion"]}
원하는 스타일: {outfit["styleMood"]}
추가 요청: {outfit["extraRequest"]}

아래 형식을 지켜서 한국어로 답해줘.

오늘의 추천 코디

상의:
하의:
아우터:
신발:
추천 색 조합:

날씨를 고려한 이유:
스타일을 고려한 이유:

체형과 퍼스널 컬러는 절대적인 규칙으로 판단하지 말고
코디를 제안할 때 참고 요소로만 활용해.

날씨와 사용자의 실제 요청과 취향을 가장 우선해서
현실적으로 입을 수 있는 코디를 추천해줘.
"""

    url = "https://copa.codyssey.kr/v1/chat/completions"

    request_data = {
        "model": "gpt-5-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    body = json.dumps(
        request_data
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        result = json.loads(
            response.read().decode("utf-8")
        )

    return result["choices"][0]["message"]["content"]


class handler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):

        body = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(body)


    def do_GET(self):

        self.send_json(
            200,
            {
                "message":
                "WeatherFit outfit API is working!"
            }
        )


    def do_POST(self):

        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            request_body = self.rfile.read(
                content_length
            )

            data = json.loads(
                request_body.decode("utf-8")
            )

            # 서버 측 입력값 검증
            if not isinstance(data, dict):
                self.send_json(
                    400,
                    {
                        "message": "잘못된 요청 형식입니다."
                    }
                )
                return

            required_sections = ["weather", "user", "outfit"]

            for section in required_sections:
                if section not in data or not isinstance(data[section], dict):
                    self.send_json(
                        400,
                        {
                            "message": f"필수 입력값이 누락되었습니다: {section}"
                        }
                    )
                    return

            if not data["weather"]:
                self.send_json(
                    400,
                    {
                        "message": "날씨 정보가 필요합니다."
                    }
                )
                return

            required_user_fields = ["bodyType", "personalColor", "height"]

            for field in required_user_fields:
                if data["user"].get(field) in [None, ""]:
                    self.send_json(
                        400,
                        {
                            "message": f"필수 사용자 정보가 누락되었습니다: {field}"
                        }
                    )
                    return

            required_outfit_fields = ["occasion", "styleMood"]

            for field in required_outfit_fields:
                if data["outfit"].get(field) in [None, ""]:
                    self.send_json(
                        400,
                        {
                            "message": f"필수 코디 정보가 누락되었습니다: {field}"
                        }
                    )
                    return

            ai_result = generate_outfit_with_ai(
                data
            )

            self.send_json(
                200,
                {
                    "message":
                    "AI 코디 추천이 완료되었습니다!",

                    "recommendation":
                    ai_result
                }
            )


        except urllib.error.HTTPError as error:

            error_detail = error.read().decode(
                "utf-8",
                errors="replace"
            )

            self.send_json(
                500,
                {
                    "message":
                    "AI API 호출 중 오류가 발생했습니다.",

                    "error":
                    error_detail
                }
            )


        except Exception as error:

            self.send_json(
                500,
                {
                    "message":
                    "데이터 처리 중 오류가 발생했습니다.",

                    "error":
                    str(error)
                }
            )