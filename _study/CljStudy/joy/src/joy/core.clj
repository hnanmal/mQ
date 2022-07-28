(ns joy.core
  (:gen-class))


:a-keyword
::also-a-keyword

(defn pour [lb ub]
  (cond
    (= ub :toujours) (iterate inc lb)
    :else (range lb ub)))

(pour 1 10)

(pour 1 :toujours)

::not-in-ns
:not-in-ns

(identical? 'goat 'goat)
(= 'goat 'goat)
(name 'goat)

(let [x 'goat, y x]
  (identical? x y))

(let [x (with-meta 'goat {:ornery true})
      y (with-meta 'goat {:ornery false})]
  [(= x y)
   (identical? x y)
   (meta x)
   (meta y)])

(defn best [f xs]
  (reduce #(if (f % %2) % %2) xs))

(best > [1 3 4 2 7 5 3])
(best < [1 3 4 2 7 5 3])

#"an example pattern"

(class #"example")
(java.util.regex.Pattern/compile "\\d")

(re-seq #"\w+" "one-two/three")




(defn -main
  "I don't do a whole lot ... yet."
  [& args])

