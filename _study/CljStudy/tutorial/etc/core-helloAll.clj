;; (ns tutorial.core
;;   (:require [clojure.string :as str])
;;   (:gen-class))

;; ;; (defn math-stuff
;; ;;   []
;; ;;   (println (+ 1 2 3))
;; ;;   (println (- 5 3 2))
;; ;;   (println (/ 10 5))
;; ;;   (println (mod 12 5))

;; ;;   (println (rand-int 20))

;; ;;   (reduce + [1 2 3])
;; ;;   (println Math/PI)
;; ;;   )

;; (defn say-hello
;;   "Receives a name with 1 parameter and responds"
;;   [name]

;;   (println "Hello again" name)
;;   )

;; (defn get-sum
;;   [x y]
;;   (println (+ x y))
;;   )
;; (defn get-sum-more
;;   ([x y z]
;;    (println (+ x y z)))
  
;;   ([x y]
;;    (println (+ x y)))
;;   )

;; (defn hello-you
;;   [name]

;;   (str "Hello " name)  
;;   )

;; (defn hello-all
;;   [& names]
;;   (map hello-you names)
;;   )

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]
;;   (say-hello "Derek")
;;   (get-sum 4 5)
;;   (get-sum-more 1 2 3)
;;   (hello-all "Doug" "mary" "Paul")
  
;;   ) 
