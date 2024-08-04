(ns clj-todo.core
  (:require [seesaw.core :as seesaw]
            [seesaw.mig :as mig])
  (:import [javax.swing JSlider]
           [java.awt Color Dimension]))

(def todos (atom []))

(defn make-todo [id description]
  {:id id :description description :done false})

(defn refresh-todo-list [listbox]
  (seesaw/config! listbox :model (map :description @todos)))

(defn add-todo-handler [text-field hour-slider minute-slider listbox]
  (let [text (seesaw/text text-field)
        hour (str (.getValue hour-slider))
        minute (str (.getValue minute-slider))
        time (str hour ":" minute)]
    (when (not (empty? text))
      (swap! todos conj (make-todo (count @todos) (str text " at " time)))
      (refresh-todo-list listbox)
      (seesaw/text! text-field ""))))

(defn remove-todo-handler [listbox]
  (let [selected (seesaw/selection listbox)]
    (when selected
      (swap! todos (fn [ts] (remove #(= (:description %) selected) ts)))
      (refresh-todo-list listbox))))

(defn create-slider [min max init major-tick minor-tick]
  (let [slider (seesaw/slider :min min :max max :value init
                              :major-tick-spacing major-tick
                              :minor-tick-spacing minor-tick
                              :paint-ticks? true
                              :paint-labels? true)]
    (seesaw/config! slider :preferred-size (Dimension. 300 50))
    slider))

(defn create-ui []
  (let [input-panel (seesaw/flow-panel :background (Color. 173 216 230)) ;; Light blue
        todo-panel (seesaw/flow-panel :background (Color. 255 182 193)) ;; Pink
        frame (seesaw/frame
               :title "Modern TODO App"
               :content
               (mig/mig-panel
                :constraints ["fill"]
                :items [[input-panel "w 50%-10px!, grow"]
                        [todo-panel "w 50%!, grow"]])
               :on-close :exit
               :size [800 :by 400])]

    ;; Left Panel (Input Area)
    (seesaw/add! input-panel
                 [[(seesaw/label :text "Enter TODO:" :foreground (Color. 0 0 0) :font "SansSerif-16")
                  (seesaw/text :id :todo-text :border 1 :font "SansSerif-16") "growx, span"]
                 [(seesaw/button :text "Add" :id :add-btn :background (Color. 76 175 80) :foreground (Color. 255 255 255) :font "SansSerif-16") "wrap"]
                 [(seesaw/label :text "Hour:" :foreground (Color. 0 0 0) :font "SansSerif-14") "split 2"]
                 [(create-slider 0 23 12 1 1) "growx, wrap"]
                 [(seesaw/label :text "Minute:" :foreground (Color. 0 0 0) :font "SansSerif-14") "split 2"]
                 [(create-slider 0 59 0 10 1) "growx, wrap"]])

    ;; Right Panel (TODO List)
    (seesaw/add! todo-panel
                 [[(seesaw/label :text "TODOs:" :foreground (Color. 0 0 0) :font "SansSerif-16") "span 2, wrap"]
                 [(seesaw/button :text "Remove" :id :remove-btn :background (Color. 244 67 54) :foreground (Color. 255 255 255) :font "SansSerif-16") "wrap"]
                 [(seesaw/listbox :id :todo-list :font "SansSerif-16") "grow, pushy, span 2, aligny top"]])

    ;; Set background color for both panels
    (.setBackground (.getContentPane frame) (Color. 211 211 211)) ;; Light Gray
    frame))

(defn -main []
  (let [frame (create-ui)
        listbox (seesaw/select frame [:#todo-list])
        text-field (seesaw/select frame [:#todo-text])
        add-btn (seesaw/select frame [:#add-btn])
        remove-btn (seesaw/select frame [:#remove-btn])
        hour-slider (seesaw/select frame [:#hour-slider])
        minute-slider (seesaw/select frame [:#minute-slider])]
    (seesaw/listen add-btn :action (fn [_] (add-todo-handler text-field hour-slider minute-slider listbox)))
    (seesaw/listen remove-btn :action (fn [_] (remove-todo-handler listbox)))
    (seesaw/listen text-field :key-pressed
                   (fn [e]
                     (when (= (.getKeyCode e) java.awt.event.KeyEvent/VK_ENTER)
                       (add-todo-handler text-field hour-slider minute-slider listbox))))
    (seesaw/show! frame)))
