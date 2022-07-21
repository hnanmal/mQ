(ns joy.core
  (:gen-class))

(defn initial-board
  []
  [\r \n \b \q \k \b \n \r
   \p \p \p \p \p \p \p \p
   \- \- \- \- \- \- \- \-
   \- \- \- \- \- \- \- \-
   \- \- \- \- \- \- \- \-
   \- \- \- \- \- \- \- \-
   \P \P \P \P \P \P \P \P
   \R \N \B \Q \K \B \N \R])

(def ^:dynamic *file-key* \a)
(def ^:dynamic *rank-key* \0)

(defn- file-component [file]
  (- (int file) (int *file-key*)))

(defn- rank-component [rank]
  (->> (int *rank-key*)
       (- (int rank))
       (- 8)
       (* 8)))

(defn- index [file rank]
  (+ (file-component file) (rank-component rank)))

(defn lookup [board pos]
  (let [[file rank] pos]
    (board (index file rank))))


(lookup (initial-board) "c3")

;;;;

`(+ 10 (* 3 2))
`(+ 10 ~(* 3 2))

(let [x 2]
  `(1 ~x 3))
(let [x 2]
  `(1 x 3))


(let [x '(2 3)] `(1 ~x))
(let [x '(2 3)] `(1 ~@x))

`portion#
`portion#
;;;;

(defn print-down-from [x]
  (when (pos? x)
    (println x)
    (recur (dec x))))

(defn sum-down-from [sum x]
  (if (pos? x)
    (recur (+ sum x) (dec x))
    sum))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (sum-down-from 0 10))

java.util.Locale/KOREA
(Math/sqrt 9)

(new java.awt.Point 0 1)
(java.awt.Point. 1 2)

(def tmp (java.util.HashMap. {"foo" 42 "bar" 3 "baz" "quux"}))

(.-x (java.awt.Point. 10 20))
(.divide (java.math.BigDecimal. "42") 2M)