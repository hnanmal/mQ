(ns joy.mutation
  (:import java.util.concurrent.Executors))

(def thread-pool    ; CPU 개수보다 2개 많은 스레드 풀 생성
  (Executors/newFixedThreadPool
   (+ 2 (.availableProcessors (Runtime/getRuntime)))))

(defn dothreads!
  [f & {thread-count :threads    ; 스레드 개수
        exec-count :times    ; 함수 실행 횟수
        :or {thread-count 1 exec-count 1}}]     ; 기본값 지정
  (dotimes [t thread-count]
    (.submit thread-pool
             #(dotimes [_ exec-count] (f)))))    ; 함수 호출


(dothreads! #(.print System/out "Hi ") :threads 2 :times 2)

;;;;;예제 10.1 클로저의 ref를 사용한 3 x 3 체스 보드 표현

(def initial-board    ; 초기 시드(seed)는 벡터의 벡터
  [[:- :k :-]
   [:- :- :-]
   [:- :K :-]])

(defn board-map [f board]
  (vec (map #(vec (for [s %] (f s)))
            board)))    ; 각 셀은 자신의 참조로 구성

(defn reset-board!
  "보드 상태를 리셋한다. 일반적으로 이러한 방식의 함수가 권장되지는 않지만,
   지면의 제한을 고려해야 했다."
  []
  (def board (board-map ref initial-board))
  (def to-move (ref [[:K [2 1]] [:k [0 1]]]))
  (def num-moves (ref 0)))

(defn neighbors
  ([size yx] (neighbors [[-1 0] [1 0] [0 -1] [0 1]]
                        size
                        yx))
  ([deltas size yx]
   (filter (fn [new-yx]
             (every? #(< -1 % size) new-yx))
           (map #(vec (map + yx %))
                deltas))))


(def king-moves    ; 킹이 가능한 이동 정의
  (partial neighbors
           [[-1 -1] [-1 0] [-1 1] [0 -1] [0 1] [1 -1] [1 0] [1 1] [1 1]] 3))

(defn good-move?
  [to enemy-sq]
  (when (not= to enemy-sq)    ; to 가 점령되어 있으면 nil 리턴
    to))

(defn choose-move
  "적절한 이동을 랜덤하게 선택"
  [[[mover mpos] [_ enemy-pos]]]
  [mover (some #(good-move? % enemy-pos)    ; 첫 번째 가능한 이동 선택
               (shuffle (king-moves mpos)))])  ; 가능한 이동 목록을 섞음


(reset-board!)
(take 5 (repeatedly #(choose-move @to-move)))