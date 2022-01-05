;; (ns hello-seesaw.core
;;   (:gen-class))

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]
;;   (println "Hello, World!"))

(ns hello-seesaw.core
  (:gen-class)
  (:require [seesaw.core :as seesaw]))

;; (defn currency-of
;;   [[_ currency]]
;;   currency)
;; (defn -main
;;   [& args]
;;   (currency-of 1))

;; (fn [x] (* 2 x))

(def window (seesaw/frame
             :title "First Example"
             :content "hello world!! Hello MK!!!!"
             :width 1000
             :height 500))
(defn -main
  [& args]
  (seesaw/show! window))