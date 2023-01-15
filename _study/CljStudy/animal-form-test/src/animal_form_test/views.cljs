(ns animal-form-test.views
  (:require
   [re-frame.core :as re-frame]
   [animal-form-test.subs :as subs]
   ))

(defn text-input []
  [:div.field
   [:label.label "Name"]
   [:div.control
    [:input.input {:type "text" :placeholder "Text input"}]]])

(defn select-input []
  [:div.field
   [:label.label "Subject"]
   [:div.control
    [:div.select
     [:select
      [:option "Select dropdown"]
      [:option "With options"]]]]])

(defn main-panel []
  (let [name (re-frame/subscribe [::subs/name])]
    [:div
     [:h1
      "Hello from, " @name]
     [text-input]
     [select-input]
     ]))
