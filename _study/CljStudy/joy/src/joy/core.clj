(ns joy.core
  (:gen-class)
  (:require [clojure.string :as str-]))


;; 3.3.2 벡터로 구조분해 하기
;; 이번에는 Guy의 이름 각 부분을 사용하기 좀 더 편리하게 만들기 위해 let으로 구조분해해서
;; 로컬을 생성해보자
(def guys-whole-name ["Guy" "Lewis" "Steele"])

(let [[f-name m-name l-name] guys-whole-name]
  (str l-name ", " f-name " " m-name))

(clojure.string/upper-case "sss")

(let [s "Eric Normand"
      s (str-/upper-case s)
      s (str-/trim s)
      s (str-/replace s #" +" "-")
      ]
  (println s))


(defn -main
  "I don't do a whole lot ... yet."
  [& args])