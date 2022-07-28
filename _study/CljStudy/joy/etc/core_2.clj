(ns joy.core
  (:gen-class))

(defn xors [max-x max-y]
  (for [x (range max-x) y (range max-y)]
    [x y (rem (bit-xor x y) 256)]))

(def frame (java.awt.Frame.))
frame

(for [meth (.getMethods java.awt.Frame)
      :let [name (.getName meth)]
      :when (re-find #"Vis" name)]
  name)

(.isVisible frame)
(.setVisible frame true)
(.setSize frame (java.awt.Dimension. 200 200))

(def gfx (.getGraphics frame))

(.setColor gfx (java.awt.Color. 255 128 0))
(.fillRect gfx 100 150 75 50)

;; (doseq [[x y xor] (xors 200 200)]
;;   (.setColor gfx (java.awt.Color. xor xor xor))
;;   (.fillRect gfx x y 1 1))

(defn clear [g] (.clearRect g 0 0 200 200))

(clear gfx)

(doseq [[x y xor] (xors 500 500)]
  (.setColor gfx (java.awt.Color. xor xor xor))
  (.fillRect gfx x y 1 1))

:a-keyword
::also-a-keyword

(defn pour [lb ub]
  (cond
    (= ub :toujours) (iterate inc lb)
    :else (range lb ub)))

(pour 1 10)

(pour 1 :toujours)

::not-in-ns
:not-in-ns

(identical? 'goat 'goat)
(= 'goat 'goat)
(name 'goat)

(let [x 'goat, y x]
  (identical? x y))

(let [x (with-meta 'goat {:ornery true})
      y (with-meta 'goat {:ornery false})]
  [(= x y)
   (identical? x y)
   (meta x)
   (meta y)])



(defn -main
  "I don't do a whole lot ... yet."
  [& args])

