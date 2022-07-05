(ns my-pjt.core
  (:gen-class))

(import java.time.LocalDate)

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  ;; (println (. LocalDate now)))
  (println
   (str (LocalDate/now))))


(-main)