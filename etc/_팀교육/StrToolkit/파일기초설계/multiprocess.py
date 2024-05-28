import multiprocessing
import time

# 작업 함수: 리스트의 요소를 제곱
def square(number):
    return number * number

# 병렬 처리 함수
def parallel_square(numbers):
    # 프로세스 풀 생성
    with multiprocessing.Pool(processes=4) as pool:  # 4개의 프로세스를 사용하여 병렬 처리
        # 병렬 처리 실행
        results = pool.map(square, numbers)
    return results

if __name__ == "__main__":
    # 큰 리스트 생성
    numbers = list(range(1, 1000000))

    # 시작 시간 기록
    start_time = time.time()

    # 병렬 처리 함수 호출
    results = parallel_square(numbers)

    # 종료 시간 기록
    end_time = time.time()

    # 결과 출력 (처리 시간)
    print(f"Processing time: {end_time - start_time} seconds")
