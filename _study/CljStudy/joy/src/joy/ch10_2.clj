(ns joy.ch10-2)

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

(defn place [from to] to)

(defn move-piece [[piece dest] [[_ src] _]]
  (alter (get-in board dest) place piece)  ; 이동하는 말을 위치시킴
  (alter (get-in board src) place :-)
  (alter num-moves inc))

(defn update-to-move [move]
  (alter to-move #(vector (second %) move)))  ; 새 위치로 교체

(defn make-move []
  (let [move (choose-move @to-move)]
    (dosync (move-piece move @to-move))  ; 한 트랜잭션에서는 보드와 num-moves를 업데이트하고
    (dosync (update-to-move move))))  ; 다른 트랜잭션에서(주의할 것)는 to-move를 업데이트함

