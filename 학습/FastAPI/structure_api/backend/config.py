from fastapi.middleware.cors import CORSMiddleware


def add_cors(app, origins: list[str] | None = None):
    origins = origins or [
        "http://localhost:5173",  # Vite dev
        "http://127.0.0.1:5173",
        # 배포 시 Nginx 경유 동일 오리진이면 생략 가능
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
