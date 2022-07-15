;; (ns tutorial.core
;;   (:require [clojure.string :as str])
;;   (:gen-class))

;; (use 'clojure.java.io)

;; (defn destruct
;;   []
;;   (def vectVals [1 2 3 4])
;;   (let [[one two & the-rest] vectVals]
;;     (println one two the-rest)))

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]

;;   (destruct)
;; ) 
