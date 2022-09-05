(ns joy.ch5_6
  (:gen-class)
  (:require [clojure.string :as str-]))

;; 5.6.1 해시 맵
(hash-map :a 1, :b 2, :c 3, :d 4, :e 5)

(let [m {:a 1, 1 :b, [1 2 3] "4 5 6"}]
  [(get m :a) (get m [1 2 3])])
