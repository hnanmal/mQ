(ns animal-form.views
  (:require
   [re-frame.core :as re-frame]
   [animal-form.subs :as subs]
   ))

(defn main-panel []
  (let [name (re-frame/subscribe [::subs/name])]
    [:div
     [:h1
      "Hello from " @name]
     ]))
