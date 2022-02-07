(ns helloworld.core
  (:gen-class))

(defn -main [& args]
;; (def b 10)
;; (println
;;   (if (> b 2)
;;     "b는 2보다 크다."
;;     "b는 2보다 크지 않다."))
(defn hello
	[]
	(def a 3))

(hello)
(println a)
)

(-main)