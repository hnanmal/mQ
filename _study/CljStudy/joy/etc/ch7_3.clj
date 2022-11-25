;; (ns joy.ch7_3)

;; (defn pow [base exp]
;;   (if (zero? exp)
;;     1
;;     (* base (pow base (dec exp)))))

;; (pow 2 10)


;; (pow 1.01 925)


;; (pow 2 10000)


;; (defn pow [base exp]
;;   (letfn [(kapow [base exp acc]
;;                  (if (zero? exp)
;;                    acc
;;                    (recur base (dec exp) (* base acc))))]
;;     (kapow base exp 1)))

;; (pow 2N 10000)


;; (def simple-metric {:meter 1,
;;                     :km 1000,
;;                     :cm 1/100,
;;                     :mm [1/10 :cm]})

;; (->       (* 3  (:km simple-metric))
;;        (+ (* 10 (:meter simple-metric)))
;;        (+ (* 80 (:cm simple-metric)))
;;        (+ (* (:cm simple-metric)
;;              (* 10 (first (:mm simple-metric)))))
;;        float)

;; ;;;;
;; (defn convert [context descriptor]
;;   (reduce (fn [result [mag unit]]  ; (1)구조분해
;;             (+ result
;;                (let [val (get context unit)]  ; (2) 미터 기준 상대적 값 조회
;;                        (if (vector? val)
;;                          (* mag (convert context val))  ; (3) 단위 변환 처리
;;                          (* mag val)))))  ; (4) 최종 변환 값 계산
;;           0
;;           (partition 2 descriptor)))

;; (convert simple-metric [1 :meter])


;; (convert simple-metric [50 :cm])


;; (convert simple-metric [100 :mm])

;; (float (convert simple-metric 
;;                 [3 :km 10 :meter 80 :cm 10 :mm]))


;; (convert {:bit 1, :byte 8, :nibble [1/2 :byte]} [32 :nibble])

;; ;;;
;; (defn gcd [x y]
;;   (cond
;;     (> x y) (gcd (- x y) y)
;;     (< x y) (gcd x (- y x))
;;     :else x))

;; (gcd 175681756817568 6543265432)

;; (defn gcd [x y]
;;   (int
;;    (cond
;;      (> x y) (recur (- x y) y)
;;      (< x y) (recur x (- y x))
;;      :else x)))

;; (defn recur-gcd [x y]
;;   (cond
;;     (> x y) (recur (- x y) y)
;;     (< x y) (recur x (- y x))
;;     :else x))

;; (recur-gcd 175681756817568 6543265431)

;; ;;;;;;;

;; (defn elevator [commands]
;;   (letfn
;;    [(ff-open [[_ & r]]
;;              "엘리베이터가 1층에서 문이 열려있으면 문을 닫거나 종료할 수 있다."
;;              #(case _
;;                 :close (ff-closed r)
;;                 :done true
;;                 false))
;;     (ff-closed [[_ & r]]
;;                "엘리베이터가 1층에서 문이 닫혀있으면 문을 열거나 올라갈 수 있다."
;;                #(case _
;;                   :open (ff-open r)
;;                   :up (sf-closed r)
;;                   false))
;;     (sf-closed [[_ & r]]
;;                "엘리베이터가 2층에서 문이 닫혀있으면 문을 열거나 내려갈 수 있다."
;;                #(case _
;;                   :down (ff-closed r)
;;                   :open (sf-open r)
;;                   false))
;;     (sf-open [[_ & r]]
;;              "엘리베이터가 2층에서 문이 열려있으면 문을 닫거나 종료할 수 있다."
;;              #(case _
;;                 :close (sf-closed r)
;;                 :done true
;;                 false))]
                
;;                 (trampoline ff-open commands)))

;; (elevator [:close :open :close :up :open :open :done])


;; (elevator [:close :up :open :close :down :open :done])


;; ;; 아래 코드는 종료되지 않으니 주의해서 실행할 것
;; (elevator (cycle [:close :open]))

;; (+ 1 2)

;; ;;;;

;; (defn fac-cps [n k]
;;   (letfn [(cont [v] (k (* v n)))]  ; 다음(Continuation)
;;     (if (zero? n)  ; 연산 종료 조건(Accept)
;;       (k 1)  ; 리턴(Return)
;;       (recur (dec n) cont))))

;; (defn fac [n]
;;   (fac-cps n identity))

;; (fac 10)


;; (defn mk-cps [accept? kend kont]
;;   (fn [n]
;;     ((fn [n k]
;;        (let [cont (fn [v]  ; 다음(Continuation)
;;                   (k ((partial kont v) n)))]
;;          (if (accept? n)  ; 연산 종료 조건(Accept)00
;;            (k 1)  ; 리턴 값(Return)
;;            (recur (dec n) cont))))
;;      n kend)))

;; (def fac  ; 팩토리얼 함수
;;   (mk-cps zero?  ; 0이면 종료
;;           identity  ; 종료 시 1을 리턴
;;           #(* %1 %2)))  ; 스택의 숫자들을 곱함

;; (fac 10)


;; (def tri  ; 트라이앵글 함수
;;   (mk-cps #(== 1 %)  ; 1이면 종료
;;           identity  ; 종료 시 0을 리턴
;;           #(+ %1 %2)))  ; 스택의 숫자들을 더함

;; (tri 10)

;; (tri 15)

;; ;;;;