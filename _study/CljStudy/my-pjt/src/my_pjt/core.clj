(ns my-pjt.core
  (:gen-class)
  (:require [clojure.java.io :as io]))

(import java.time.LocalDate)
(use 'dk.ative.docjure.spreadsheet)

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  ;; (println (. LocalDate now)))
  ;; (println
  ;;   (str (LocalDate/now)))

  (print 
    (->> (load-workbook-from-file "11.xlsx")
       (select-sheet "Sheet1")
       (select-columns {:A :name, :B :price})))
  )