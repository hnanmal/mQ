;; (ns tutorial.core
;;   (:require [clojure.string :as str])
;;   (:gen-class))

;; (defn atom-ex
;;   [x]

;;   (def atomEx (atom x))

;;   (add-watch atomEx :watcher
;;        (fn [key atom old-state new-state]
;;          (println "atomEx changed from " 
;;                   old-state " to " new-state)))
  
;;   (println "1st x" @atomEx)
;;   (reset! atomEx 10)
;;   (println "2nd x" @atomEx)
;;   (swap! atomEx inc)
;;   (println "Increment x" @atomEx)
;;   )

;; (defn agent-ex
;;   []
  
;;   (def tickets-sold (agent 0))
;;   (send tickets-sold + 15)
;;   ;; (println)
;;   (await-for 100 tickets-sold) 
;;   (println "Tickets " @tickets-sold)

;;   (send tickets-sold + 10)
;;   (await-for 100 tickets-sold)
;;   (println "Tickets " @tickets-sold)

;;   ;; (shutdown-agents)

;;   )

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]

;;   ;; (atom-ex 5)
;;   (agent-ex) 

;;   ) 
