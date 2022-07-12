;; (ns tutorial.core
;;   (:require [clojure.string :as str])
;;   (:gen-class))

;; (defn one-to-x
;;   [x]
;;   (def i (atom 1))
;;   (while (<= @i x)
;;     (do
;;       (println @i)
;;       (swap! i inc))))

;; (defn dbl-to-x
;;   [x]
;;   (dotimes [i x]
;;     (println (* i 2))))

;; (defn triple-to-x
;;   [x y]
;;   (loop [i x]
;;     (when (< i y)
;;       (println (* i 3))
;;       (recur (+ i 1)))))

;; (defn print-list
;;   [& nums]
;;   (doseq [x nums]
;;     (println x)))

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]
;;   (one-to-x 5)
;;   (dbl-to-x 5)
;;   (triple-to-x 0 5)
;;   (print-list 7 8 9)
;;   ) 
