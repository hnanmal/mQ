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

(def form
  (grid-panel :columns 2
              :items ["First Name" (text :id :first-name)
                      "Last Name" (text :id :last-name)
                      "Sex" (combobox :id :sex
                                      :model ["Female" "Male"])
                      "Age" (spinner :id :age)]))

(defn -main [& args]
  (invoke-later
   (->
    ;; (frame :title "Hello",
    ;;           ;; :content "Hello, Seesaw",
    ;;           :content safety,
    ;;           :on-close :exit) 
    (frame :title "Why Swing, why?",
           :on-close :exit
          ;;  :content (label :text "Hiya"
          ;;                  :border [100 "Compound" 10]
          ;;                  :background "#999"
          ;;                  :foreground :blue)
          ;;  :content (slider :min 0
          ;;                   :max 11
          ;;                   :value 6
          ;;                   :background "#999"
          ;;                   :foreground :blue)
           :content form
           )
    pack!
    show!)))