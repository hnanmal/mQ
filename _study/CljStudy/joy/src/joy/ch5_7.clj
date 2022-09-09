(ns joy.ch5-7
  (:gen-class)
  (:require [clojure.string :as str-]))

(defn pos [e coll]
  (let [cmp (if (map? coll)
              #(= (second %1) %2)
              #(= %1 %2))]
    (loop [s coll idx 0]
      (when (seq s)
        (if (cmp (first s) e)
          (if (map? coll)
            (first (first s))
            idx)
          (recur (next s) (inc idx)))))))

(pos 3 [:a 1 :b 2 :c 3 :d 4])

(pos :foo [:a 1 :b 2 :c 3 :d 4])

(pos 3 {:a 1 :b 2 :c 3 :d 4})

(pos \3 ":a 1 :b 2 :c 3 :d 4")


(defn index [coll]
  (cond
    (map? coll) (seq coll)
    (set? coll) (map vector coll coll)
    :else (map vector (iterate inc 0) coll)))

(index [:a 1 :b 2 :c 3 :d 4])

(index {:a 1 :b 2 :c 3 :d 4})

(index #{:a 1 :b 2 :c 3 :d 4})

(defn pos [e coll]
  (for [[i v] (index coll) :when (= e v)] i))

(pos 3 [:a 1 :b 2 :c 3 :d 4])

(pos 3 {:a 1 :b 2 :c 3 :d 4})

(pos 3 [:a 3 :b 3 :c 3 :d 4])

(pos 3 {:a 3 :b 3 :c 3 :d 4})


(defn pos [pred coll]
  (for [[i v] (index coll) :when (pred v)] i))


(pos #{3 4} {:a 1 :b 2 :c 3 :d 4})

(pos even? [2 3 6 7])

(even? 3)