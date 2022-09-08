(ns joy.ch5_6
  (:gen-class)
  (:require [clojure.string :as str-]))

;; 5.6.1 해시 맵
(hash-map :a 1, :b 2, :c 3, :d 4, :e 5)

(let [m {:a 1, 1 :b, [1 2 3] "4 5 6"}]
  [(get m :a) (get m [1 2 3])])

(let [m {:a 1, 1 :b, [1 2 3] "4 5 6"}]
  [(m :a) (m [1 2 3])])

(seq {:a 1, :b 2})

(into {} [[:a 1] [:b 2]])

(into {} (map vec '[(:a 1) (:b 2)]))

(apply hash-map [:a 1 :b 2])

(zipmap [:a :b] [1 2])

;; 5.6.2 sorted-map으로 키 값 정리하기

(sorted-map :thx 1138 :r2d 2)

(sorted-map "bac" 2 "abc" 9)

(sorted-map-by #(compare (subs %1 1) (subs %2 1)) "bac" 2 "abc" 9)

(sorted-map :a 1 "b" 2)

(assoc {1 :int} 1.0 :float)

(assoc (sorted-map 1 :int) 1.0 float)

;; 5.6.3 배열 맵으로 입력 순서 유지하기

(seq (hash-map :a 1 :b 2 :c 3))

(seq (array-map :a 1 :b 2 :c 3))