(ns joy.ch7-4)

(defn neighbors
  ([size yx] (neighbors [[-1 0] [1 0] [0 -1] [0 1]]
                        size
                        yx))
  ([deltas size yx]
   (filter (fn [new-yx]
             (every? #(< -1 % size) new-yx))
           (map #(vec (map + yx %))
                deltas))))



(def world [[  1   1   1   1   1]
            [999 999 999 999   1]
            [  1   1   1   1   1]
            [  1 999 999 999 999]
            [  1   1   1   1   1]])

(neighbors 5 [0 0])

(defn estimate-cost [step-cost-est size y x]
  (* step-cost-est
     (- (+ size size) y x 2)))

(estimate-cost 900 5 0 0)


(estimate-cost 900 5 4 4)


(defn path-cost [node-cost cheapest-nbr]
  (+ node-cost
     (or (:cost cheapest-nbr) 0)))  ; 가장 싼 이웃 비용이나 0을 비용에 추가

(path-cost 900 {:cost 1})


(defn total-cost [newcost step-cost-est size y x]
  (+ newcost
     (estimate-cost step-cost-est size y x)))

(total-cost 0 900 5 0 0)


(total-cost 1000 900 5 3 4)


(total-cost (path-cost 900 {:cost 1}) 900 5 3 4)


(defn min-by [f coll]
  (when (seq coll)
    (reduce (fn [min other]  ; 각 항목 처리
              (if (> (f min) (f other))  ; 계속해서 작은 값을 리턴하도록 함
                other
                min))
            coll)))

(min-by :cost [{:cost 100} {:cost 36} {:cost 9}])


(repeat 10 nil)
;;;;;;;;;;
(defn astar [start-yx step-est cell-costs]
  (let [size (count cell-costs)]
    (loop [steps 0
           routes (vec (repeat size (vec (repeat size nil))))
           work-todo (sorted-set [0 start-yx])]
      (if (empty? work-todo)  ; 끝났는지 확인
        [(peek (peek routes)) :steps steps]  ; 첫번째 경로 선택
        (let [[_ yx :as work-item] (first work-todo)  ; 다음 작업 항목을 받아옴
              rest-work-todo (disj work-todo work-item)  ; 작업 목록에서 삭제
              nbr-yxs (neighbors size yx)  ; 이웃 받아오기
              cheapest-nbr (min-by :cost  ; 최소 비용 계산
                                   (keep #(get-in routes %)
                                         nbr-yxs))
              newcost (path-cost (get-in cell-costs yx)  ; 현재까지 비용 계산
                                 cheapest-nbr)
              oldcost (:cost (get-in routes yx))]
          (if (and oldcost (>= newcost oldcost))  ; 새 비용과 기존 비용 비교
            (recur (inc steps) routes rest-work-todo)
            (recur (inc steps)  ; 노선에 새 경로를 포함시킴
                   (assoc-in routes yx
                             {:cost newcost
                              :yxs (conj (:yxs cheapest-nbr [])
                                         yx)})
                   (into rest-work-todo  ; 작업 목록에 추정된 경로를 추가하고 재귀
                         (map
                          (fn [w]
                           (let [[y x] w]
                             [(total-cost newcost step-est size y x) w]))
                         nbr-yxs)))))))))


(astar [0 0]
       900
       world)

(astar [0 0]
       900
       [[1    1    1    2    1]  ; 약한 관목이 있는 길
        [1    1    1  999    1]
        [1    1    1  999    1]
        [1    1    1  999    1]
        [1    1    1    1    1]])  ; 아무것도 없는길


(astar [0 0]
       900
       [[1    1    1    2    1]  ; 약한 관목이 있는 길
        [1    1    1  999    1]
        [1    1    1  999    1]
        [1    1    1  999    1]
        [1    1    1  666    1]])  ; 식인종이 기다리고 있음