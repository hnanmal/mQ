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

(let [s (-> `"Eric Normand"
     (str-/upper-case)
     (str-/trim))] 
  (str-/replace s #" +" "-"))

(let [[a b c & more] (range 10)]
  (println "a b c are:" a b c)
  (println "more is:" more))

(let [range-vec (vec (range 10))
      [a b c & more :as all-] range-vec]
  (println "a b c are:" a b c)
  (println "more is:" more)
  (println "all is:" all-))

(def guys-name-map 
  {:f-name "Guy" :m-name "Lewis" :l-name "Steele"})

(let [{f-name :f-name, m-name :m-name} guys-name-map]
  (str " ," f-name " " m-name))

(let [{:keys [m-name f-name]} guys-name-map]
  (str " ," f-name " " m-name))

(let [{f-name :f-name, :as whole-name} guys-name-map]
  (println "First name is" f-name)
  (println "Whole name is" whole-name))

(let [{:keys [title f-name m-name l-name], 
       :or {title "Mr. "}} guys-name-map]
  (println title f-name m-name l-name))

(defn whole-name [& args]
  (let [{:keys [f-name m-name l-name]} args]
    (str l-name " ," f-name " " m-name)))

(whole-name :f-name "Guy" :l-name "Steele" :m-name "Lewis")

(let [{first-thing 0, last-thing 3} [1 2 3 4]]
  [first-thing last-thing])
;;;
(defn print-last-name [{:keys [l-name]}]
  (println l-name))
(print-last-name guys-name-map)

;; (defn print-last-name2 [args]
;;   (let [{:keys [l-name]} args]
;;     (println l-name))
;;   )
;; (print-last-name2 guys-name-map)


(defn -main
  "I don't do a whole lot ... yet."
  [& args])