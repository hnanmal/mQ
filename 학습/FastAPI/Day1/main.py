# app.py
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Korean Advice Proxy (author + '선생님')")

SOURCE_URL = "https://korean-advice-open-api.vercel.app/api/advice"
TIMEOUT_SEC = 8


def append_teacher_suffix(name: str) -> str:
    if not name:
        return "무명 선생님"
    # 이미 '선생님'으로 끝나면 중복 방지
    if name.endswith("선생님"):
        return name
    return f"{name} 선생님"


@app.get("/advice")
def get_advice():
    try:
        r = requests.get(SOURCE_URL, timeout=TIMEOUT_SEC)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"업스트림 연결 실패: {e}")

    if r.status_code != 200:
        raise HTTPException(
            status_code=502, detail=f"업스트림 상태 코드: {r.status_code}"
        )

    try:
        data = r.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="업스트림 응답이 JSON이 아닙니다.")

    # 다양한 스키마를 안전하게 처리
    # 일반적으로 {"id":..., "advice":"...", "author":"..."} 형태가 많지만
    # author가 없을 수도 있어 대비
    author = None
    for key in ("author", "writer", "name"):
        if isinstance(data, dict) and key in data:
            author = data.get(key)
            break

    # author 필드 붙이기
    fixed_author = append_teacher_suffix(author)

    # 원본 구조를 최대한 유지하되 author를 보정
    if isinstance(data, dict):
        # author 계열 키가 하나도 없었다면 'author' 키로 추가
        if author is None:
            data["author"] = fixed_author
        else:
            # 어떤 키로 들어왔는지 찾은 뒤 그 자리에 업데이트
            for key in ("author", "writer", "name"):
                if key in data:
                    data[key] = fixed_author
                    break
        # 원본 출처도 함께 알려주면 디버깅에 유용
        data["_source"] = SOURCE_URL
        return data

    # 혹시 배열/기타 형태면 간단히 래핑해서 반환
    return {
        "advice": data,
        "author": fixed_author,
        "_source": SOURCE_URL,
    }


@app.get("/health")
def health():
    return {"ok": True}
