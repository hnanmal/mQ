@ECHO OFF

REM 파일 목록을 저장할 파일 경로를 지정합니다.
SET "파일경로=%CD%\result.txt"

REM 파일 목록을 저장합니다.
ECHO "현재 폴더의 파일 목록을 저장합니다..."
DIR /b > %파일경로%
ECHO "저장이 완료되었습니다."