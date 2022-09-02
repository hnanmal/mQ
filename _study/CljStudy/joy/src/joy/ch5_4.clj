(ns joy.ch5_4
  (:gen-class)
  (:require [clojure.string :as str-]))

(defmethod print-method clojure.lang.PersistentQueue
  [q, w]

  (print-method '<- w)
  (print-method (seq q) w)
  (print-method '-< w))

clojure.lang.PersistentQueue/EMPTY


;; 5.4.2 입력하기

(def schedule
  (conj clojure.lang.PersistentQueue/EMPTY
        :wake-up :shower :brush-teeth))

schedule

;; 5.4.3 꺼내기
(peek schedule)

;; 5.4.4 삭제하기
(pop schedule)

(rest schedule)