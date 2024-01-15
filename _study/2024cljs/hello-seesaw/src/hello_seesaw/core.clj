(ns hello-seesaw.core
  (:use seesaw.core))

(require '[seesaw.bind :as b])

(def safety
  (checkbox :text "Safety"
             :selected? true))

(def fire-missiles 
  (button :text "Fire!"
          :enabled? false))

(b/bind
 safety
 (b/property fire-missiles :enabled?))

(defn foo
  "I don't do a whole lot."
  [x]
  (println x "Hello, World!"))

(defn -main [& args]
  (invoke-later
   (-> (frame :title "Hello",
              ;; :content "Hello, Seesaw",
              :content safety,
              :on-close :exit)
       pack!
       show!)))