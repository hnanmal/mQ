;; (ns joy.ch6-4)

;; (defn rand-ints [n]
;;   (take n (repeatedly #(rand-int n))))


;; (rand-ints 10)


;; (defn sort-parts [work]
;;   (lazy-seq
;;    (loop [[part & parts] work]  ; work를 분리시킨다.
;;      (if-let [[pivot & xs] (seq part)]
;;        (let [smaller? #(< % pivot)]  ; pivot을 비교하는 함수 정의
;;          (recur (list*
;;                  (filter smaller? xs)  ; pivot보다 작은 경우의 처리
;;                  pivot  ; pivot 자신에 대한 처리
;;                  (remove smaller? xs)  ; pivot 보다 큰 경우의 처리
;;                  parts)))  ; parts 접근
;;        (when-let [[x & parts] parts]
;;          (cons x (sort-parts parts)))))))  ; parts가 더 있으면 나머지도 정렬

;; (defn qsort [xs]
;;   (sort-parts (list xs)))

;; (qsort [2 1 4 3])

;; (qsort (rand-ints 20))

;; (first (qsort (rand-ints 20)))

;; (take 10 (qsort (rand-ints 10000)))