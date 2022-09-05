(ns joy.ch5_5
  (:gen-class)
  (:require [clojure.string :as str-]
            [clojure.set :as c-set]))

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


(def my-set (sorted-set :a :b))

;; ... 다른 코드들을 작성하고 난 후

(conj my-set "a")

;; 5.5.3 contains? 함수

(contains? #{1 2 4 3} 4)

(contains? [1 2 4 3] 4)

;; 5.5.4 clojure.set 네임스페이스

(:require 'clojure.set)


(ns joy.ch5_5
  (:require [clojure.set :as c-set]))

;; 교집합 (intersection) 함수
(clojure.set/intersection #{:humans :fruit-bats :zombies}
                    #{:chupacabra :zombies :humans})

(clojure.set/intersection #{:pez :gum :dots :skor}
                          #{:pez :skor :pocky}
                          #{:pocky :gum :skor})



;; 합집합 (union) 함수

(clojure.set/union #{:humans :fruit-bats :zombies}
                   #{:chupacabra :zombies :humans})

(clojure.set/union #{:pez :gum :dots :skor}
                   #{:pez :skor :pocky}
                   #{:pocky :gum :skor})


;; 차집합 (difference) 함수

;; 실제로는 이렇게 동작하지 않는다

(clojure.set/difference #{1 2 3 4} #{3 4 5 6})