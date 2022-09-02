(ns joy.ch5_5
  (:gen-class)
  (:require [clojure.string :as str-]))

;; 5.5.1 클로저 셋의 기본적인 특성
(#{:a :b :c :d} :c)

(#{:a :b :c :d} :e)

(get #{:a 1 :b 2} :b)

(get #{:a 1 :b 2} :z :nothing-doing)

;;; 클로저 셋에 값 입력하는 방법

(into #{[]} [()])

(into #{[1 2]} '([1 2]))

(into #{[] #{} {}} [()])


;;;; 셋과 some 함수를 사용해서 시퀀스 내 항목 찾기

(some #{:b} [:a 1 :b 2])


(some #{1 :b} [:a 1 :b 2])


;; 5.5.2 셋 순서대로 유지하기: sorted-set

(sorted-set :b :c :a)

(sorted-set [3 4] [1 2])

(sorted-set :b 2 :c :a 3 1)