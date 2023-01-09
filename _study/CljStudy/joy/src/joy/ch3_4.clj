(ns joy.ch3-4 
  (:require [clojure.java.javadoc :as javadoc]
            [clojure.repl :refer [find-doc]]))

(range 5)

(for [x (range 2) y (range 2)] [x y])

(xor 1 2)

(find-doc "xor")

(bit-xor 1 2)

(bit-xor 1 1)

(for [x (range 2) y (range 2)] 
  [x y (bit-xor x y)])

(defn xors [max-x max-y]
  (for [x (range max-x) y (range max-y)]
    [x y (bit-xor x y)]))

(xors 2 2)


(def frame (java.awt.Frame.))

frame

(for [meth (.getMethods java.awt.Frame)   ; ① 클래스 메서드를 순회
      :let [name (.getName meth)]           ; ② var 이름을 바인딩
      :when (re-find #"Vis" name)]             ; ③ 찾은 이름들을 시퀀스로 구성
  name)

(.isVisible frame)

(.setVisible frame true)

(.setSize frame (java.awt.Dimension. 200 200))

frame

(javadoc/javadoc frame)

(def gfx (.getGraphics frame))

(.fillRect gfx 100 100 50 75)

(.setColor gfx (java.awt.Color. 255 128 0))
(.fillRect gfx 100 150 75 50)


(doseq [[x y xor] (xors 200 200)]
  (.setColor gfx (java.awt.Color. xor xor xor))
  (.fillRect gfx x y 1 1))

(doseq [[x y xor] (xors 500 500)]
  (.setColor gfx (java.awt.Color. xor xor xor))
  (.fillRect gfx x y 1 1))

(defn xors [max-x max-y]
  (for [x (range max-x) y (range max-y)]
    [x y (rem (bit-xor x y) 256)]))

(defn clear [g] (.clearRect g 0 0 200 200))

(clear gfx)

(doseq [[x y xor] (xors 500 500)]
  (.setColor gfx (java.awt.Color. xor xor xor))
  (.fillRect gfx x y 1 1))