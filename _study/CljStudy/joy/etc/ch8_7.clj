;; (ns joy.ch8-7)

;; (declare collect-bodies)

;; (defn build-contract [c]
;;   (let [args (first c)]
;;     (list
;;      (into '[f] args)
;;      (apply merge
;;             (for [con (rest c)]
;;               (cond (= (first con) 'require)
;;                     (assoc {} :pre (vec (rest con)))
;;                     (= (first con) 'ensure)
;;                     (assoc {} :post (vec (rest con)))
;;                     :else (throw (Exception.,
;;                                   (str "Unknown tag "
;;                                        (first con)))))))
;;      (list* 'f args))))

;; (fn doubler 
;;   ([f x]
;;    {:post [(= (* 2 x) %)],
;;     :pre [(pos? x)]}
;;    (f x)))


;; (defmacro contract [name & forms]
;;   (list* `fn name (collect-bodies forms)))

;; (defn collect-bodies [forms]
;;   (for [form (partition 3 forms)]
;;     (build-contract form)))

;; (def doubler-contract  ; contract 정의
;;   (contract doubler
;;             [x]
;;             (require
;;              (pos? x))
;;             (ensure
;;              (= (* 2 x) %))))

;; (def times2 (partial doubler-contract #(* 2 %)))  ; 올바른 사용 테스트

;; (times2 9)

;; (def times3 (partial doubler-contract #(* 3 %)))  ; 잘못된 사용 테스트

;; (times3 9)


;; ;;;

;; (def doubler-contract  ; contract 정의
;;   (contract doubler
;;             [x]  ; 인자가 하나인 contract 정의
;;             (require
;;              (pos? x))
;;             (ensure
;;              (= (* 2 x) %))
;;             [x y]  ; 인자가 2 개인 contract 정의
;;             (require 
;;              (pos? x)
;;              (pos? y))
;;             (ensure
;;              (= (* 2 (+ x y)) %))))

;; ((partial doubler-contract #(* 2 (+ %1 %2))) 2 3)  ; 올바른 사용 테스트


;; ((partial doubler-contract #(+ %1 %1 %2 %2)) 2 3)  ; 잘못된 사용 테스트


;; ((partial doubler-contract #(* 3 (+ %1 %2))) 2 3)  ; 잘못된 함수 테스트