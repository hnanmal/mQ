;; (ns joy.ch7-2)

;; ;;;;;7.2

;; (def times-two
;;   (let [x 2]
;;     (fn [y] (* y x))))

;; (times-two 5)

;; (def add-and-get
;;   (let [ai (java.util.concurrent.atomic.AtomicInteger.)]
;;     (fn [y] (.addAndGet ai y))))

;; (add-and-get 2)

;; (add-and-get 2)

;; (add-and-get 7)

;; (defn times-n [n]
;;   (let [x n]
;;     (fn [y] (* y x))))

;; (times-n 4)

;; (def times-four (times-n 4))

;; (times-four 10)

;; (defn times-n [n]
;;   (fn [y] (* y n)))

;; (defn divisible [denom]
;;   (fn [num]
;;     (zero? (rem num denom))))

;; ((divisible 3) 6)


;; ((divisible 3) 7)

;; ;;;
;; (filter even? (range 10))

;; (filter (divisible 4) (range 10))

;; (defn filter-divisible [denom s]
;;   (filter (fn [num] (zero? (rem num denom))) s))

;; (filter-divisible 4 (range 10))


;; (defn filter-divisible [denom s]
;;   (filter #(zero? (rem % denom)) s))

;; (filter-divisible 5 (range 20))

;; ;;;
;; (def bearings [{:x 0, :y 1}  ; 북쪽
;;                {:x 1, :y 0}  ; 동쪽
;;                {:x 0, :y -1}  ; 남쪽
;;                {:x -1, :y 0}])  ;서쪽

;; (defn forward [x y bearing-num]
;;   [(+ x (:x (bearings bearing-num)))
;;    (+ y (:y (bearings bearing-num)))])

;; (forward 5 5 0)

;; (forward 5 5 1)


;; (forward 5 5 2)

;; (defn bot [x y bearing-num]
;;   {:coords [x y]
;;    :bearing ([:north :east :south :west] bearing-num)
;;    :forward (fn [] (bot (+ x (:x (bearings bearing-num)))
;;                         (+ y (:y (bearings bearing-num)))
;;                         bearing-num))})

;; (:coords (bot 5 5 0))

;; (:bearing (bot 5 5 0))


;; (defn bot [x y bearing-num]
;;   {:coords [x y]
;;    :bearing ([:north :east :south :west] bearing-num)
;;    :forward (fn [] (bot (+ x (:x (bearings bearing-num)))
;;                         (+ y (:y (bearings bearing-num)))
;;                         bearing-num))
;;    :turn-right (fn [] (bot x y (mod (+ 1 bearing-num) 4)))
;;    :turn-left  (fn [] (bot x y (mod (- 1 bearing-num) 4)))})


;; (:bearing ((:forward ((:forward ((:turn-right (bot 5 5 0))))))))


;; (:coords ((:forward ((:forward ((:turn-right (bot 5 5 0))))))))


;; (defn mirror-bot [x y bearing-num]
;;   {:coords [x y]
;;    :bearing ([:north :east :soouth :west] bearing-num)
;;    :forward (fn [] (mirror-bot (- x (:x (bearings bearing-num)))
;;                                (- y (:y (bearings bearing-num)))
;;                                bearing-num))
;;    :turn-right (fn [] (mirror-bot x y (mod (- 1 bearing-num) 4)))
;;    :turn-left  (fn [] (mirror-bot x y (mod (+ 1 bearing-num) 4)))})

;; (:bearing ((:forward ((:forward ((:turn-right (mirror-bot 5 5 0))))))))


;; (:coords ((:forward ((:forward ((:turn-right (mirror-bot 5 5 0))))))))


;; ;;;

