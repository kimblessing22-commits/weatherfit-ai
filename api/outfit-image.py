from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error


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
        timeout=90
    ) as response:

        result = json.loads(
            response.read().decode("utf-8")
        )

    image_b64 = (
        result["result"]
        ["images"][0]
        ["b64_json"]
    )

    return image_b64


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
                "WeatherFit image API is working!"
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


        except urllib.error.HTTPError as error:

            error_detail = error.read().decode(
                "utf-8",
                errors="replace"
            )

            self.send_json(
                500,
                {
                    "message":
                    "이미지 AI API 호출 중 오류가 발생했습니다.",

                    "error":
                    error_detail
                }
            )


        except Exception as error:

            self.send_json(
                500,
                {
                    "message":
                    "이미지 처리 중 오류가 발생했습니다.",

                    "error":
                    str(error)
                }
            )