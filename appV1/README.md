# APP V1
## Docker 관리
- Docker Compose를 통해 여러 서비스를 동시에 실행
    - 서비스 시작 명령어
    ```bash
    docker-compose up -d
    ```
    - 서비스 중지 명령어
    ```bash
    docker-compose down
    ```


## 접근
Konga 관리 UI: http://localhost:5004
Kong Admin API: http://localhost:8001
Flask 앱: http://localhost:8000
Kong Proxy (API Gateway): http://localhost:5005