(ns animal-form-test.views
  (:require
   [re-frame.core :as rf]
   [animal-form-test.events :as events]
   [animal-form-test.subs :as subs]
   [re-frame.core :as re-frame]))
   

(def animal-types ["Dog" "Cat" "Mouse"])

(defn animal-list []
  (let [animals @(re-frame/subscribe [::subs/animals])]
    [:div
     [:h2
      [:strong "< Animal List >"]]
     [:ul
      (map (fn [{:keys [animal-type animal-name]}]
             [:li {:key animal-name} (str animal-name "(" animal-type ")")]) animals)]]))
    

(defn text-input [id label]
  (let [value @(rf/subscribe [::subs/form id])]
   [:div.field
    [:label.label label]
    [:div.control
     [:input.input {:value value
                    :on-change #(rf/dispatch [::events/update-form id (-> % .-target .-value)])
                    :type "text" :placeholder "Text input"}]]]))
  

(defn select-input [id label options]
  (let [value (rf/subscribe [::subs/form id])]
    [:div.field
     [:label.label label]
     [:div.control
      [:div.select
       [:select {:value @value
                 :on-change #(rf/dispatch [::events/update-form id (-> % .-target .-value)])}
        [:option {:value ""} "Please select"]
        (map (fn [o] [:option {:key o :value o} o]) options)]]]]))

(defn main-panel []
  (let [name @(rf/subscribe [::subs/name])
        is-valid? @(rf/subscribe [::subs/form-is-valid? [:animal-name :animal-type]])]
    [:div.section
     [:h1.title
      "Hello from, " name]
     [animal-list]
     [text-input :animal-name "Animal Name"]
     [select-input :animal-type "Animal Type" animal-types]
     [:button.button.is-primary {:disabled (not is-valid?)
                                 :on-click #(rf/dispatch [::events/save-form])} "save"]]))
     
