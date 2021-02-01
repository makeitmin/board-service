# Board Service

다양한 API를 구현하여 게시판 웹 서비스를 제공하는 프로젝트입니다.

## Getting Started

### Environment
아래 사항들은 프로젝트를 개발하는 환경입니다.
* Windows 10
* Visual Studio Code

### Prerequisites

아래 사항들이 로컬에 설치가 되어야 합니다.
* MySQL Server(+Workbench) 8.0
* Python 3.9
```
choco install mysql mysql.workbench python --y 
```

### Installing
아래 명령어로 프로젝트에 필요한 Python Packages를 설치할 수 있습니다.
```
pip install flask flask-restful pymysql 
```
MySQL Server 또는 MySQL Workbench에서 ```initial_schema.sql```을 통해 필요한 테이블과 레코드를 초기화할 수 있습니다.
```
create table if not exists board(..);
create table if not exists boardArticle(...);
create table if not exists user(...);
...
```

## Running
1. ```app.py```를 실행합니다.
2. http://127.0.0.1:5000/board 에 접속합니다.

### APIs
아래 사항은 구현된 API 항목들에 대한 설명입니다.
| API | 기능 |
| --- | --- |
| User APIs | 사용자 회원가입/로그인/로그아웃 관리 |
| Board APIs | 게시판 관리 |
| BoardArticle APIs | 게시판 내 작성글 관리 |
| Dashboard APIs | 작성글을 대시보드로 관리 |

## Issues
- [ ] Internal Error 발생
    ```TypeError: The view function did not return a valid response. The function either returned None or ended without a return statement.```
- [ ] Board APIs 에서 Read API 실행 시 한글 깨짐 발생