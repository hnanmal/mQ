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

(let [origin (java.awt.Point. 0 0)]
  (set! (.-x origin) 15)
  (str origin))

(.endsWith (.toString (java.util.Date.)) "2022")

(.. (java.util.Date.) toString (endsWith "2022"))

(doto (java.util.HashMap.)
  (.put "Home" "/home/me")
  (.put "SRC" "src")
  (.put "BIN" "classes"))
;; => {"SRC" "src", "BIN" "classes", "Home" "/home/me"}


(->
 2
 (+ 3)
 (- 7))

(-> 
 (java.util.Date.)
 (.toString)
 (.endsWith "2022")
 )

(throw (Exception. "I done throwed"))

(defn throw-catch [f]
  [(try
     (f)
     (catch ArithmeticException e "No dividing by zero!")
     (catch Exception e (str "You are so bad " (.getMessage e)))
     (finally (println "returning...")))])

(throw-catch #(/ 10 5))

(throw-catch #(throw (Exception. "Crybaby")))

;;;;;;

(seq [1 2 3])
(seq [])
(seq '(1 3 5))

(defn print-seq [s]
  (when (seq s)
    (prn (first s))
    (recur (rest s))))

(print-seq [1 1 1])

(def guys-whole-name ["Guy" "Lewis" "Steele"])

(let [[f-name m-name l-name] guys-whole-name]
  (str l-name ", " f-name ", " m-name))

(let [[a b c & more] (range 10)]
  (println "a b c are:" a b c)
  (println "more is:" more))

(let [range-vec (vec (range 10))
      [a b c & more :as all] range-vec]
  (println "a b c are:" a b c)
  (println "more is:" more)
  (println "all is:" all))


(def guys-name-map
  {:f-name "Guy" :m-name "Lewis" :l-name "Steele"})

(let [{f-name :f-name, m-name :m-name, l-name :l-name} guys-name-map]
  (str l-name ", " f-name " " m-name))



(let [{:keys [f-name m-name l-name]} guys-name-map]
  (str l-name ", " f-name " " m-name))

(let [{f-name :f-name, :as whole-name} guys-name-map]
  (println "First name is" f-name)
  (println "Whole name is below:")
  whole-name)

(let [{:keys [title f-name m-name l-name],
       :or {title "Mr."}} guys-name-map]
  (println title f-name m-name l-name))

(defn whole-name [& args]
  (let [{:keys [f-name m-name l-name]} args]
    (str l-name ", " f-name " " m-name)))

(whole-name :f-name "Guy" :m-name "Lewis" :l-name "Steele")


(use '[clojure.set :only (index)])
(def weights #{{:name 'betsy :weight 1000}
               {:name 'jake :weight 756}
               {:name 'shyq :weight 1000}})

(def by-weight (index weights [:weight]))

by-weight

{
 {:weight 1000} 
 #{{:name shyq, :weight 1000} {:name betsy, :weight 1000}}, 
 {:weight 756} 
 #{{:name jake, :weight 756}}}