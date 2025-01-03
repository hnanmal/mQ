;; (ns joy.ch7-1
;;   (:require [clojure.test :as t]))

;; (map
;;  [:chthon :phthor :beowulf :grendel]
;;  #{0 3})

;; (map
;;  [:chthon :phthor :beowulf :grendel]
;;  [0 3])

;; (map
;;  [:chthon :phthor :beowulf :grendel]
;;  '(0 3))

;; ;;;
;; (def fifth (comp first rest rest rest rest))
;; (fifth [1 2 3 4 5])

;; (defn fnth [n]
;;   (apply comp
;;          (cons first
;;                (take (dec n) (repeat rest)))))

;; ((fnth 5) '[a b c d e])

;; (cons first
;;       (take (dec 4) (repeat rest)))

;; (apply comp
;;        (cons first
;;              (take (dec 4) (repeat rest))))

;; (map (comp  ; 함수 구성
;;       keyword  ; 키워드 생성
;;       #(.toLowerCase %)  ; 소문자로 변환
;;       name)  ; 이름을 string으로 리턴
;;      '(a B C))  ; 합성한 함수를 심벌의 리스트에 맵핑

;; ;;;
;; ((partial + 5) 100 200)

;; ;;;
;; (let [truthiness (fn [v] v)]
;;   [((complement truthiness) true)
;;    ((complement truthiness) 42)
;;    ((complement truthiness) false)
;;    ((complement truthiness) nil)])


;; ((complement even?) 2)

;; ;;;
;; (defn join
;;   {:test (fn []
;;            (assert
;;             (= (join "," [1 2 3]) "1,3,3")))}
;;   [sep s]
;;   (apply str (interpose sep s)))


;; (defn ^:private ^:dynamic sum [nums]
;;   (map + nums))

;; (defn ^{:private true, :dynamic true} sum [nums]
;;   (map + nums))

;; (defn sum {:private true, :dynamic true} [nums]
;;   (map + nums))

;; (defn sum
;;   ([nums]
;;    (map + nums))
;;   {:private true, :dynamic true})


;; (use '[clojure.test :as t])
;; (t/run-tests)

;; ;;;
;; (sort [1 5 7 0 -42 13])

;; (sort ["z" "x" "a" "aa"])


;; (sort [(java.util.Date.) (java.util.Date. 100)])


;; (sort [[1 2 3], [-1, 0, 1], [3 2 1]])


;; (sort > [7 1 4])

;; (sort ["z" "x" "a" "aa" 1 5 8])


;; (sort [{:age 99}, {:age 13}, {:age 7}])

;; (sort [[:a 7], [:c 13], [:b 21]])

;; (sort second [[:a 7], [:c 13], [:b 21]])

;; (sort-by second [[:a 7], [:c 13], [:b 21]])

;; (sort-by str ["z" "x" "a" "aa" 1 5 8])

;; (sort-by :age [{:age 99}, {:age 13}, {:age 7}])


;; (def plays [{:band "Burial" :plays 979, :loved 9},
;;             {:band "Eno" :plays 2333, :loved 15},
;;             {:band "Bill Evans" :plays 979, :loved 9},
;;             {:band "Magma" :plays 2665, :loved 31}])

;; (def sort-by-loved-ratio (partial sort-by #(/ (:plays %) (:loved %))))

;; (sort-by-loved-ratio plays)

;; ;;;
;; (defn columns [column-names]
;;   (fn [row]
;;     (vec (map row column-names))))

;; (sort-by (columns [:plays :loved :band]) plays)

;; (columns [:plays :loved :band])

;; ((columns [:plays :loved :band])
;;  {:band "Burial", :plays 979, :loved 9})

;; ;;;
;; (defn keys-apply [f ks m]
;;   (let [only (select-keys m ks)]
;;     (zipmap (keys only)
;;             (map f (vals only)))))

;; (keys-apply #(.toUpperCase %) #{:band} (plays 0))

;; (defn manip-map [f ks m]
;;   (merge m (keys-apply f ks m)))

;; (manip-map #(int (/ % 2)) #{:plays :loved} (plays 0))


;; (defn slope
;;   [& {:keys [p1 p2] :or {p1 [0 0] p2 [1 1]}}]
;;   (float (/ (- (p2 1) (p1 1))
;;             (- (p2 0) (p1 0)))))

;; (slope :p1 [4 15] :p2 [3 21])


;; (slope :p2 [2 1])


;; (slope)

;; ;;;
;; (defn slope [p1 p2]
;;   {:pre [(not= p1 p2) (vector? p1) (vector? p2)]
;;    :post [(float? %)]}
;;   (/ (- (p2 1) (p1 1))
;;      (- (p2 0) (p1 0))))

;; (slope [10 10] [10 10])


;; (slope [10 1] '(1 20))


;; (slope [10 1] [1 20])


;; (slope [10.0 1] [1 20])


;; ;;;
;; (defn put-things [m]
;;   (into m {:meat "beef" :veggie "broccoli"}))

;; (put-things {})


;; (defn vegan-constraints [f m]
;;   {:pre [(:veggie m)]
;;    :post [(:veggie %) (nil? (:meat %))]}
;;   (f m))

;; (vegan-constraints put-things {:veggie "carrot"})

;; (defn balanced-diet [f m]
;;   {:post [(:meat %) (:veggie %)]}
;;   (f m))

;; (balanced-diet put-things {})


;; (defn finicky [f m]
;;   {:post [(= (:meat %) (:meat m))]}
;;   (f m))

;; (finicky put-things {:meat "chicken"})


