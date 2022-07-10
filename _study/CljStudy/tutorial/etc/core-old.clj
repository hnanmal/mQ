;; (ns tutorial.core-old
;;   (:require [clojure.string :as str])
;;   (:gen-class))


;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]

;;   ;; (def aString "Hello")
;;   ;; (def aDouble 1.234)
;;   ;; (def aLong 15)
;;   ;; (format "This is string %s" aString)
;;   ;; (format "5 spaces and %5d" aLong)
;;   ;; (format "Leading zeros %04d" aLong)
;;   ;; (format "%-4d left justified" aLong)
;;   ;; (format "3 decimals %.3f" aDouble)

;;   (def str1 "This is my 2nd string")
;;   (str/blank? str1)
;;   (str/includes? str1 "my")
;;   (str/index-of str1 "my")
;;   (str/split str1 #" ")
;;   (str/split str1 #"\d")
;;   (str/join " " ["The" "Big" "Cheese"])
;;   (str/replace "I am 42" #"42" "43")
;;   (str/upper-case str1)
;;   (str/lower-case str1)

;;   (println (list "Dog" 1 3.4 true))
;;   (println (nth (list 1 2 3) 1))
;;   (println (list* 1 2 [3 4]))
;;   (println (cons 3 (list 1 2)))

;;   (println (get (set '(3 2)) 2))
;;   (println (conj (set '(3 2)) 1))
;;   (println (contains? (set '(3 2)) 2))
;;   (println (disj (set '(3 2)) 2))

;;   (println (get (vector 3 2) 1))
;;   (println (conj (vector 3 2) 1))
;;   (println (pop (vector 3 2)))
;;   (println (subvec (vector 1 2 3 4) 1 3))

;;   (println (hash-map "Name" "Derek" "Age" 42))
;;   (println (sorted-map 3 42 2 "Banas" 1 "Derek"))
;;   (println (get (hash-map "Name" "Derek") "Name"))
;;   (println (contains? (hash-map "Name" "Derek" "Age" 42) "Age"))
;;   (println (keys (hash-map "Name" "Derek" "Age" 42)))
;;   (println (vals (hash-map "Name" "Derek" "Age" 42)))
;;   (println (merge-with + (hash-map "Name" "Derek") (hash-map "Age" 42)))

;;   )
