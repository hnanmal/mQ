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


  (println
  (->> (load-workbook-from-file ".\\11.xlsx") ;; (load-workbook "building_list.xlsx")
        (select-sheet "Sheet1")
        (select-columns {:B :first :C :third})
        (remove nil?)
        ;; row-seq
        ;; (remove nil?)
        ;; (map cell-seq)
        ;; (map #(map read-cell %))
        ))

      ;;  (select-columns {:B :name, :C :price})
  )