;; (ns tutorial.core
;;   (:require [clojure.string :as str])
;;   (:gen-class))

;; (defn can-vote
;;   [age]
;;   (if (>= age 18)
;;     (println "You can vote")
;;     (println "You can't vote")))

;; (defn can-do-more
;;   [age]
;;   (if (>= age 18)
;;     (do (println "You can drive")
;;         (println "You can Vote"))
;;     (println "You can't vote")))

;; (defn when-ex
;;   [tof]
;;   (when tof
;;     (println "1st thing")
;;     (println "2nd thing")))

;; (defn what-grade
;;   [n]
;;   (cond
;;     (< n 5) (println "Preschool")
;;     (= n 5) (println "Kindergarten")
;;     (and (> n 5) (<= n 18)) (format "Go to grade %d" (- n 5))
;;     :else "Go to College"))

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]

;;   (can-vote 19)
;;   (can-do-more 24)
;;   (when-ex true)
;;   (what-grade 19)
;;   (what-grade 17)
  
;;   ) 
