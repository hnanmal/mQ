(ns hello-seesaw.core
  (:use seesaw.core))

(require '[seesaw.bind :as b])

(def safety
  (checkbox :text "Safety"
             :selected? true))

(def fire-missiles 
  (button :text "Fire!"
          :enabled? false))
;; (+ 2 3)
(b/bind
 safety
 (b/property fire-missiles :enabled?))

(defn foo
  "I don't do a whole lot."
  [x]
  (println x "Hello, World!"))

(def form
  (grid-panel :columns 3
              :items ["[1]" "First Name" (text :id :first-name)
                      "[2]" "Last Name" (text :id :last-name)
                      "[3]" "Sex" (combobox :id :sex
                                            :model ["Female" "Male" "Attack Helicopter"])
                      "[4]" "Age" (spinner :id :age)]
              :border [30 "Compound" 10]))

(defn -main [& args]
  (invoke-later
   (->
    (frame :title "Why Swing, why?",
           :on-close :exit
           :menubar 
           (menubar :items [(menu
                             :text "File" 
                             :items 
                             ["Open" "save"])])
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

(+ 1 2 3 4 5)
(reduce + [1 2 3])

(def example-dict 
  {:a "good!"
   :b "nice~"
   :c "cute~"})

(:a example-dict)
(example-dict :a)

(def blank-dict {})

(def next-dict (assoc blank-dict 
                      :title "Is this right?"
                      :on-close :exit
                      :content "king-ah!"
            ))

(next-dict :title)
(next-dict :on-close)
(next-dict :content)
(:title next-dict)
(:on-close next-dict)
(:content next-dict)

(= [:a :b :c] (list :a :b :c) (vec '(:a :b :c)) (vector :a :b :c))
[:a :b :c]

(list :a :b :c)
(vec '(:a :b :c))
(vector :a :b :c)

(= [:a :b :c] (list :a :b :c) )

(conj '(1 2 3) 4)

(conj [1 2 3] 4)
(set '(:a :a :b :c :c :c :c :d :d))
(conj #{1 4 3} 2)

(def x 
  {:a 10
   :b 20
   :c 30})

(= 20 ((hash-map :a 10, :b 20, :c 30) :b))

(first x)
(x :b)