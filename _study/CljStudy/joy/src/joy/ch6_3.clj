(ns joy.ch6-3
  (:gen-class)
  (:require [clojure.string :as str-]
            [clojure.test :as t]))

(- 13 (+ 2 2))

(defn if-chain [x y z]
  (if x
    (if y
      (if z
        (do
          (println "Made it!")
          :all-truthy)))))

(if-chain () 42 true)



(if-chain true true false)

(defn and-chain [x y z]
  (and x y z (do
               (println "Made it!!")
               :all-truthy)))

(and-chain () 42 true)



(and-chain true false true)

;;(steps [1 2 3 4])


(defn rec-step [[x & xs]]
  (if x
    [x (rec-step xs)]
    []))

(rec-step [1 2 3 4])

(rec-step (range 200000))

(def very-lazy
  (-> 
   (iterate #(do (print \.) (inc %)) 1)
   rest rest rest))

(def less-lazy
  (->
   (iterate #(do (print \.) (inc %)) 1)
   next next next))

(println (first very-lazy))

(println (first less-lazy))