(ns four-clojure.core
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))

(def aa (sorted-set 5 7 2 7))

(defn mk-reverse [col]
  (let [a (map-indexed (fn [idx item] [idx item]) col)]
       (map last (into (sorted-map-by > ) a))))

(mk-reverse [1 2 3])

(mk-reverse aa)

;; Problem 26 Fibonacci Sequence
(defn fibo [n]
  (loop [cnt 1
         acc '(1 1)]
    (if (> (+ 2 cnt) n) 
      (reverse acc)
      (recur (inc cnt) (cons (+ (first acc) (fnext acc)) acc)))))


(fibo 7)

;; Problem 27
(reverse "race")
(def my-char-seq (reverse "race"))
(apply str my-char-seq)

(defn chk-palin [col]
  (let [src (apply str col)
        rev (apply str (reverse col))]
    (= src rev)))

(chk-palin '(1 2 3 4 5))
(chk-palin "racecar")
(chk-palin [:foo :bar :foo])
(chk-palin '(1 1 3 3 1 1))
(chk-palin '(:a :b :c))


;; Problem 28

(defn flatten_mk [col]
  (filter #(not (coll? %)) (tree-seq coll? identity col)))

(flatten_mk '((1 2) 3 [4 [5 6]]))



(defn sum-up-with-recur [coll result]
  (if (empty? coll) result
      (recur (rest coll) (+ result (first coll)))))

(defn do-flat [tgt]
  (if (coll? tgt)
    (map (apply (fn [x] x) tgt))
    tgt))

(def targetColl '((1 2) 3 [4 [5 6]]))
(def acc '())
(first targetColl)
(first (first targetColl))
(map #(conj acc (first %)) (first targetColl))


(do-flat [1])
(last [1 2 3])
(pop [1 2 3])

(first [1 2 3])
(rest [1 2 3])

(nfirst [[1 2] 2 3])

(filter #(not (seq? %)) (tree-seq seq? identity '((1 2 (3)) (4))))

(tree-seq coll? identity '((1 2 (3)) (4)))

;; Problem 29

(def target "HeLlO, WoRlD!")

(defn get-caps [strs]
  (->>
   strs
   list*
   (map #(re-find #"\w" (str %)))
   (filter #(not (nil? %)))
   (filter #(not (re-find  #"[0-9.]+" (str %))))
   (filter (fn [x] (= (str x) (clojure.string/upper-case x))))
   (apply str) 
   ))

(get-caps target)
(get-caps "$#A(*&987Zf")

(sequence target)
(seq target)
(filter (fn [x] (= (str x) (clojure.string/upper-case x))) (seq target))

(= "C" (clojure.string/upper-case \c))
(clojure.string/upper-case "c")


(map #(not (re-find #"[0-9.]+" (str %))) (seq "$#A(*&987Zf"))

(type (nth (map (fn [x] x) (seq "$#A(*&987Zf")) 1))

(re-find #"\w(.)" "HLO, WRD!")


;; Problem 30 Compress a Sequence

(defn comp-seq [col]
  (->>
   col
  ;;  set
   (group-by #(= (first %) (fnext %)))
   ))

(comp-seq "Leeeeeerrroyyy")
(->>
 "Leeeeeerrroyyy"
 set
 sort
 (apply str)
 )

(comp-seq [1 1 2 3 3 2 2 3])