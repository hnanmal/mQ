;; (ns joy.ch6-3
;;   (:gen-class)
;;   (:require [clojure.string :as str-]
;;             [clojure.test :as t]))

;; (- 13 (+ 2 2))

;; (defn if-chain [x y z]
;;   (if x
;;     (if y
;;       (if z
;;         (do
;;           (println "Made it!")
;;           :all-truthy)))))

;; (if-chain () 42 true)



;; (if-chain true true false)

;; (defn and-chain [x y z]
;;   (and x y z (do
;;                (println "Made it!!")
;;                :all-truthy)))

;; (and-chain () 42 true)



;; (and-chain true false true)

;; ;;(steps [1 2 3 4])


;; (defn rec-step [[x & xs]]
;;   (if x
;;     [x (rec-step xs)]
;;     []))

;; (rec-step [1 2 3 4])

;; (rec-step (range 200000))

;; (def very-lazy
;;   (-> 
;;    (iterate #(do (print \.) (inc %)) 1)
;;    rest rest rest))

;; (def less-lazy
;;   (->
;;    (iterate #(do (print \.) (inc %)) 1)
;;    next next next))

;; (println (first very-lazy))

;; (println (first less-lazy))


;; (defn lz-rec-step [s]
;;   (lazy-seq
;;    (if (seq s)
;;      [(first s) (lz-rec-step (rest s))]
;;      [])))

;; (lz-rec-step [1 2 3 4])


;; (class (lz-rec-step [1 2 3 4]))

;; (dorun (lz-rec-step (range 200000)))


;; (defn simple-range [i limit]
;;   (lazy-seq
;;    (when (< i limit)
;;      (cons i (simple-range (inc i) limit)))))


;; (simple-range 0 9)

;; ;; (let [r (range 1e9)]
;; ;;   (first r)
;; ;;   (last r))

;; ;; (let [r (range 1e9)]
;; ;;   (last r)
;; ;;   (first r))


;; ;; ; 무한 반복되는 코드이니 주의할 것
;; ;; (iterate (fn [n] (/ n 2)) 1)

;; (defn triangle [n]
;;   (/ (* n (+ n 1)) 2))

;; (triangle 10)

;; (map triangle (range 1 11))


;; (def tri-nums (map triangle (iterate inc 1)))

;; (take 10 tri-nums)  ; 앞부분 10개 숫자에 대한 삼각수 계산


;; (take 10 (filter even? tri-nums)) ; 앞 부분의 짝수 10개에 대한 삼각수 계산


;; (nth tri-nums 99) ; 가우스가 계산했던 숫자

;; (map / tri-nums)


;; (double (reduce + (take 1000 (map / tri-nums)))) ; 두 가지 연산을 조합


;; (take 2 (drop-while #(< % 10000) tri-nums))




;; (defn defer-expensive [cheap expensive]
;;   (if-let [good-enough (force cheap)]  ; 참이 리턴될 때만 then 부분을 실행
;;     good-enough
;;     (force expensive)))

;; (defer-expensive (delay :cheap)
;;                  (delay (do (Thread/sleep 5000) :expensive)))


;; (defer-expensive (delay false)
;;                  (delay (do (Thread/sleep 5000) :expensive)))


;; (if :truthy-thing
;;   (let [res :truthy-thing] (println res)))


;; (if-let [res :truthy-thing] (println res))


;; (defn inf-triangles [n]
;;   {:head (triangle n)
;;    :tail (delay (inf-triangles (inc n)))})

;; (defn head [l] (:head l))
;; (defn tail [l] (force (:tail l)))

;; (def tri-nums (inf-triangles 1))

;; (head tri-nums)

;; (head (tail tri-nums))

;; (head (tail (tail tri-nums)))


;; (defn taker [n l]
;;   (loop [t n, src l, ret []]
;;     (if (zero? t)
;;       ret
;;       (recur (dec t) (tail src) (conj ret (head src))))))

;; (defn nthr [l n]
;;   (if (zero? n)
;;     (head l)
;;     (recur (tail l) (dec n))))

;; (taker 10 tri-nums)


;; (nthr tri-nums 99)
