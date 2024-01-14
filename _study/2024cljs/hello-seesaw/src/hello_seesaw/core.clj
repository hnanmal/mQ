(ns hello-seesaw.core
  (:use seesaw.core))

(defn foo
  "I don't do a whole lot."
  [x]
  (println x "Hello, World!"))

(defn -main [& args]
  (invoke-later
   (-> (frame :title "Hello",
              :content "Hello, Seesaw",
              :on-close :exit)
       pack!
       show!)))