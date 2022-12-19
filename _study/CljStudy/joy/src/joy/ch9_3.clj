(ns joy.ch9-3 
  (:require [clojure.test :as t]))

;; {:val 5, :l nil :r nil}


;; (defrecord TreeNode [val l r])

;; (TreeNode. 5 nil nil)


;;;defstruct의 몰락

(defn change-age [p] (assoc p :age 286))

(defstruct person :fname :lname)
(change-age (struct person "Immanuel" "Kant"))

(defrecord Person [fname lname])
(change-age (Person. "Immanuel" "Kant"))

;;; ex)9.1

(defrecord TreeNode [val l r])  ; 레코드 타입 정의

(defn xconj [t v]  ; 트리에 추가
  (cond
    (nil? t)       (TreeNode. v nil nil)
    (< v (:val t)) (TreeNode. (:val t) (xconj (:l t) v) (:r t))
    :else          (TreeNode. (:val t) (:l t) (xconj (:r t) v))))

(defn xseq [t]  ; 트리를 시퀀스(seq)로 변환
  (when t
    (concat (xseq (:l t)) [(:val t)] (xseq (:r t)))))


(reduce xconj nil [3 5 2 4 6])

(def sample-tree (reduce xconj nil [3 5 2 4 6]))  ; 테스트
sample-tree
(xseq sample-tree)

(dissoc (TreeNode. 5 nil nil) :l)

;;;프로토콜

(defprotocol FIXO
  (fixo-push [fixo value])
  (fixo-pop [fixo])
  (fixo-peek [fixo]))


(extend-type TreeNode
  FIXO
  (fixo-push [node value]
    (xconj node value)))

(xseq (fixo-push sample-tree 5/2))


(extend-type clojure.lang.IPersistentVector
  FIXO
  (fixo-push [vector value]
    (conj vector value)))

(fixo-push [2 3 4 5 6] 5/2)


;;; 클로저 스타일 믹스인 (mixin)
(use 'clojure.string)

(defprotocol StringOps (rev [s]) (upp [s]))

(extend-type String
  StringOps
  (rev [s] (clojure.string/reverse s)))

(rev "Works")

(extend-type String
  StringOps
  (upp [s] (clojure.string/upper-case s)))

(upp "Works")


(rev "Works?")

(def rev-mixin {:rev clojure.string/reverse})

(def upp-mixin {:upp (fn [this] (.toUpperCase this))})

(def fully-mixed (merge upp-mixin rev-mixin))

(extend String StringOps fully-mixed)

(-> "Works" upp rev)


(rev "Works?")


(reduce fixo-push nil [3 5 2 4 6 0])

(extend-type nil
  FIXO
  (fixo-push [t v]
    (TreeNode. v nil nil)))

(reduce fixo-push nil [3 5 2 4 6 0])

(xseq (reduce fixo-push nil [3 5 2 4 6 0]))