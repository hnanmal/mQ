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
       (* 8))
  )

(defn- index [file rank]
  (+ (file-component file) (rank-component rank))
  )

(defn lookup [board pos]
  (let [[file rank] pos]
    (board (index file rank)))
  )

(lookup (initial-board) "c3")

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
