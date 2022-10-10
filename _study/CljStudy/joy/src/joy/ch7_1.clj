(ns joy.ch7-1)

(map
 [:chthon :phthor :beowulf :grendel]
 #{0 3})

(map
 [:chthon :phthor :beowulf :grendel]
 [0 3])

(map
 [:chthon :phthor :beowulf :grendel]
 '(0 3))

;;;
(def fifth (comp first rest rest rest rest))
(fifth [1 2 3 4 5])

(defn fnth [n]
  (apply comp
         (cons first
               (take (dec n) (repeat rest)))))

((fnth 5) '[a b c d e])