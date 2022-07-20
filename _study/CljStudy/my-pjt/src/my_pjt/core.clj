(ns my-pjt.core
  (:gen-class)
  ;; (:require [dk.ative.docjure.spreadsheet])
  )

(use `dk.ative.docjure.spreadsheet)
(import java.time.LocalDate)
(import java.string)

(defn value [x]
(case x
5 "x is 5"
10 "x is 10"
"x isn't 5 or 10"))
(value 11) ;;"x isn't 5 or 10"
(value 10)
(value 4)

(defprotocol StrConvert
  (to-str [this]))

(extend-protocol StrConvert
  nil
  (to-str [this] "null")
  java.lang.Integer
  (to-str [this] (str this))
  java.lang.String
  (to-str [this] (str "\"" this "\""))
  clojure.lang.Keyword
  (to-str [this] (to-str (name this)))
  java.lang.Object
  (to-str [this] (str this)))

(defn remove-line-break
  [x] 
  (cond
    (nil? x)
      "null"
    (= (type x) java.lang.String)
      (.replaceAll x "\n" " ")))
  ;; (case x
  ;;   java.lang.String (.replaceAll x "\n" " ")
  ;;   x))


(defn -main
  "I don't do a whole lot ... yet."
  [& args]

  ;;  (map #(.getNumericCellValue %)) 

  (def each-row (->> (load-workbook "building_list.xlsx")
                     (select-sheet "Building List(Rev.B)")
                     row-seq
                     (remove nil?)
                     (map cell-seq)
                     (map #(map read-cell %))
                     (map #(map remove-line-break %))))

  (def Item-3rd 
    (nth each-row 3))

  ;; ;; (println (.getNumericCellValue firstItem))
  (println (nth Item-3rd 10))
  
  
  (= (type (nth Item-3rd 10)) java.lang.String)
  )