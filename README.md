# REAL — Django + PostgreSQL starter

Uppcoder에 올리는 것을 전제로 만든 깨끗한 Django 프로젝트입니다.
로컬은 SQLite, 서버는 Uppcoder가 주입하는 `DATABASE_URL`(PostgreSQL)을 사용합니다.

## 구조

```
manage.py
config/            settings · urls · wsgi
core/              홈 화면(/), 상태 확인(/status), 관리자
static/css/        정적 파일
core/templates/    템플릿
```

## VS Code

`C:\real\real.code-workspace` 를 열면 Explorer에 **TEST (기존)** 와 **REAL (신규)** 가
동시에 표시됩니다. (파일 → 파일에서 워크스페이스 열기)

## 로컬 실행

```powershell
cd C:\real
C:\python\python.exe manage.py migrate
C:\python\python.exe manage.py runserver 8010
```

- 홈: http://127.0.0.1:8010/
- 상태: http://127.0.0.1:8010/status
- 관리자: http://127.0.0.1:8010/admin/

관리자 계정:

```powershell
C:\python\python.exe manage.py createsuperuser
```

## 환경변수

| 이름 | 로컬 | Uppcoder |
|---|---|---|
| `DEBUG` | `True` | 플랫폼이 `False` 권장 (미지정 시 False) |
| `DJANGO_SECRET_KEY` | `.env` 값 | 직접 설정 권장 |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost,testserver` | `*` 또는 실제 호스트 |
| `DATABASE_URL` | 비움 (SQLite) | 플랫폼이 자동 주입 |
| `POSTGRES_*` | 비움 | `DATABASE_URL`이 없을 때 대체 연결 정보로 사용 |
| `UPPCODER_SELF_URL` | 비움 | 플랫폼이 자동 주입 (CSRF/호스트 자동 반영) |

`.env`는 커밋하지 않습니다. 서버에서는 stack 페이지의 환경변수/Connection details를 사용하세요.

## Uppcoder 배포

1. GitHub에 새 리포지토리 생성 (private 권장)
2. 이 폴더에서 `git init -b main` → `git add .` → `git commit -m "init"` → push
3. portal.uppcoder.com → `Stacks → Create → Blank stack`
4. `Django` 검색해 추가, `PostgreSQL` 검색해 추가 (자동 연결)
5. Django 카드에 **Git repository 주소 + branch(main)** 입력, private이면 access token
6. `Deploy → Confirm and deploy`
7. stack 페이지의 Web terminal에서:

```bash
pixi run -e web-django python manage.py migrate
pixi run -e web-django python manage.py collectstatic --noinput
pixi run -e web-django python manage.py createsuperuser
```

8. stack 페이지 상단에서 `Private → Public` 전환

이후 수정은 `git push` 후 stack 페이지의 **Pull**로 반영합니다.

## 주의

- 플랫폼이 `/health`를 직접 응답하므로 상태 확인은 `/status`를 사용합니다.
- HTTPS는 프록시가 종료합니다. `SECURE_PROXY_SSL_HEADER`가 없으면 admin 로그인이 403이 됩니다(설정 완료).
- 무료 Spark는 앱 1개 + DB 1개, 2GB 메모리/디스크입니다. 미디어가 큰 사이트는 외부 스토리지가 필요합니다.
- 커스텀 도메인과 운영(Production) 환경 분리는 유료 플랜 기능입니다.
- 이 PC의 Python이 32비트이면 `psycopg[binary]` 로컬 설치가 실패할 수 있습니다. 로컬은 SQLite로 동작하므로 문제 없고, 서버(Linux)에서는 정상 설치됩니다.
