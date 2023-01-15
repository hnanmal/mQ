(ns my-reframe-test.views
  (:require
   [re-frame.core :as re-frame]
   [my-reframe-test.events :as events]
   [my-reframe-test.subs :as subs]
   [reagent.core :as r]
   ))

(defn atom-input [value]
  [:input {:type "text"
           :value @value
           :on-change #(reset! value (-> % .-target .-value))}])

(defn shared-state []
  (let [val (r/atom "foo")]
    (fn []
      [:div
       [:p "The value is now: " @val]
       [:p "Change it here: " [atom-input val]]])))

(defn counting-button [txt]
  (let [state (r/atom 0)] ;; state is accessible in the render function
    (fn [txt]
      [:button.button-8
       {:on-click #(swap! state inc)}
       (str txt " " @state)])))

(defn display-user [{:keys [id avatar email] first-name :first_name}]
  [:div.horizontal {:key id}
   [:div.pr-10
    [:img.pr-15 {:src avatar}]]
   [:div
    [:h2 first-name]
    [:p (str "(" email ")")]]
   ])

(defn main-panel []
  (let [name (re-frame/subscribe [::subs/name])
        loading (re-frame/subscribe [::subs/loading])
        users (re-frame/subscribe [::subs/users])]
    [:div
     [:h1
      "Hello from " @name]
     (when @loading "now loading...") 
     [counting-button]
     [:div.horizontal
      [:input {:type "text"
               :id "new-name"
               :value @name 
               :on-change #(reset! @name (-> % .-target .-value))}]
      [:button.button-8 {:on-click #(re-frame/dispatch [::events/update-name "My-Service"])} "Update Name"]]
     [:div.horizontal.pr-10
      [:div.pr-15
      [:button.button-8 {:on-click #(re-frame/dispatch [::events/fetch-users])} "Make API Call"]]
     [:div.pr-15
      [:button.button-8 {:on-click #(re-frame/dispatch [::events/update-name "My-Service"])} "Initialize Name"]]]
     (map display-user @users)]))
     
