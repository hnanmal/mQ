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


  ;;  (def sheet-mine 
  ;;    (->> (load-workbook-from-file "11.xlsx")
  ;;         (select-sheet "Sheet1"))) 

  ;; (->> (load-workbook "11.xlsx")
  ;;      (select-sheet "Sheet1")
  ;;      row-seq)

(println
 (->> (load-workbook "11.xlsx")
      (select-sheet "Sheet1")
      row-seq
      (remove nil?)
      (map cell-seq)
      (map #(map read-cell %))))

      ;;  (select-columns {:B :name, :C :price})
  )