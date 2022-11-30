;; (ns hello)
;; (print "hello world")
(import [numpy :as np])


(defn add_mk [x y] 
  (+ x y))

(defn make_arr [x]
  (.array np x))

(defn find_shape [arr]
  (.shape np arr))

(setv new_arr (make_arr [1 2 3]))

;; (print (find_shape new_arr))
