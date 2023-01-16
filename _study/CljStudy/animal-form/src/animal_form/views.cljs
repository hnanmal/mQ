(ns animal-form.views
  (:require
   [re-frame.core :as re-frame]
   [animal-form.subs :as subs]
   [animal-form.events :as events]
   ))

(def animal-types ["Dog" "Cat" "Mouse"])

(defn animal-list [kind]
  (let [animals @(re-frame/subscribe [::subs/animals])]
    [:div
     [:h2.subtitle (str kind "List")]
     [:ul
      (map (fn [{:keys [animal-type animal-name]}]
             [:li {:key animal-name} (str animal-name "(" animal-type ")")]) animals)]]))

(defn text-input [id label]
  (let [value (re-frame/subscribe [::subs/form id])]
    [:div.field
     [:label.label label]
     [:div.control
      [:input.input {:value @value
                     :on-change #(re-frame/dispatch [::events/update-form id (-> % .-target .-value)])
                     :type "text" :placeholder "Text input"}]]]))

(defn select-input [id label options]
  (let [value (re-frame/subscribe [::subs/form id])]
    [:div.field
     [:label.label label]
     [:div.control
      [:div.select
       [:select {:value @value
                 :on-change #(re-frame/dispatch [::events/update-form id (-> % .-target .-value)])}
        [:option {:value ""} "Please select"]
        (map (fn [o] [:option {:key o :value o} o]) options)
        ]]]]))

(defn form-regist-kind [kind x]
  [
   [:h1.title (str kind "Manager")]
   [(animal-list kind)]
   [text-input :animal-name "Animal Name"]
   [select-input :animal-type "Animal Type" animal-types]
   [:button.button.is-primary {:disabled (not x)
                               :on-click #(re-frame/dispatch [::events/save-form])} "save"]])


(defn main-panel []
  (let [is-valid? @(re-frame/subscribe [::subs/form-is-valid? [:animal-name :animal-type]])] 
    [:section.section
     [:div
      [:h1.title (str "Animal" " Manager")]
      [animal-list "Animal "]
      [text-input :animal-name "Animal Name"]
      [select-input :animal-type "Animal Type" animal-types]
      [:button.button.is-primary.is-light {:disabled (not is-valid?)
                                           :on-click #(re-frame/dispatch [::events/save-form])} "save"]]]
    ;; [:div
    ;;   [@form-regist-kind "my-animals" is-valid?]]
     ))
