(ns two-pane-app.core
  (:require [seesaw.core :as seesaw]))

(defn create-page [n]
  (let [left-panel  (seesaw/vertical-panel :items [(seesaw/label (str "Left content of Page " n))])
        right-panel (seesaw/vertical-panel :items [(seesaw/label (str "Right content of Page " n))])]
    (seesaw/left-right-split left-panel right-panel :divider-location 0.5)))

(defn create-frame []
  (let [pages (mapv (fn [n] (create-page n)) (range 1 13))
        tab-panel (seesaw/tabbed-panel
                   :tabs (mapv (fn [n page]
                                 {:title (str "Page " n)
                                  :content page})
                               (range 1 13) pages))]
    (seesaw/frame :title "Tabbed Page App"
                  :content tab-panel
                  :on-close :exit
                  :width 800
                  :height 600)))

(defn -main []
  (seesaw/invoke-later
   (seesaw/show! (create-frame))))
