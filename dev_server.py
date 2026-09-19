from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error


# -----------------------------
# .env 파일 불러오기
# -----------------------------

env_path = os.path.join(
    os.path.dirname(__file__),
    ".env"
)

if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as env_file:

        for line in env_file:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:

                key, value = line.split("=", 1)

                os.environ.setdefault(
                    key.strip(),
                    value.strip()
                )


print(
    "API key loaded:",
    bool(os.environ.get("CODYSSEY_API_KEY"))
)


# -----------------------------
# 코디세이 AI 호출
# -----------------------------

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


    url = (
        "https://copa.codyssey.kr"
        "/v1/chat/completions"
    )


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


    ai_text = (
        result["choices"][0]
        ["message"]
        ["content"]
    )


    return ai_text

def generate_outfit_image(recommendation_text):

    api_key = os.environ.get("CODYSSEY_API_KEY")

    if not api_key:
        raise Exception(
            "CODYSSEY_API_KEY가 설정되지 않았습니다."
        )


    prompt = f"""
다음 코디 추천 내용을 바탕으로
한 명의 인물이 해당 코디를 착용한 전신 패션 이미지를 생성해줘.

조건:
- 인물은 1명만 보여줘
- 추천된 상의, 하의, 아우터, 신발, 색 조합이 잘 보이게 해줘
- 깔끔한 패션 룩북 또는 패션 일러스트 느낌
- 배경은 밝고 단순하게
- 전신이 잘 보이게
- 텍스트나 워터마크는 넣지 말아줘

코디 추천:
{recommendation_text}
"""


    url = "https://copa.codyssey.kr/api/v1/images"


    request_data = {
        "model": "gpt-image-1-mini",
        "prompt": prompt,
        "size": "1024x1024",
        "response_format": "b64_json"
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
        timeout=60
    ) as response:

        result = json.loads(
            response.read().decode("utf-8")
        )


    image_b64 = result["result"]["images"][0]["b64_json"]

    return image_b64
# -----------------------------
# 로컬 개발 서버
# -----------------------------

class DevHandler(SimpleHTTPRequestHandler):

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

        if self.path == "/api/outfit":
            self.send_json(
                200,
                {
                    "message":
                    "WeatherFit Python API is working!"
                }
            )

            return

        super().do_GET()


    def do_POST(self):

        if self.path not in [
            "/api/outfit",
            "/api/outfit-image"
        ]:
            self.send_json(
                404,
                {
                    "message":
                    "요청한 API를 찾을 수 없습니다."
                }
            )

            return


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


            # 텍스트 코디 추천
            if self.path == "/api/outfit":

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

                return


            # 코디 이미지 생성
            if self.path == "/api/outfit-image":

                recommendation_text = data.get(
                    "recommendation",
                    ""
                )

                if recommendation_text.strip() == "":
                    self.send_json(
                        400,
                        {
                            "message":
                            "이미지 생성을 위한 코디 추천 내용이 없습니다."
                        }
                    )

                    return


                image_b64 = generate_outfit_image(
                    recommendation_text
                )

                self.send_json(
                    200,
                    {
                        "message":
                        "AI 코디 이미지가 생성되었습니다!",

                        "imageBase64":
                        image_b64
                    }
                )

                return


        except urllib.error.HTTPError as error:

            error_detail = error.read().decode(
                "utf-8",
                errors="replace"
            )

            print(
                "CODYSSEY API ERROR:",
                error_detail
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

            print(
                "PYTHON ERROR:",
                str(error)
            )

            self.send_json(
                500,
                {
                    "message":
                    "데이터 처리 중 오류가 발생했습니다.",

                    "error":
                    str(error)
                }
            )
if __name__ == "__main__":

    server = ThreadingHTTPServer(
        ("127.0.0.1", 8000),
        DevHandler
    )


    print(
        "WeatherFit 개발 서버 실행 중: "
        "http://127.0.0.1:8000"
    )


    server.serve_forever()