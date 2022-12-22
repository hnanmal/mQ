;; (ns joy.ch9-3 
;;   (:require [clojure.test :as t]))

;; ;; {:val 5, :l nil :r nil}


;; ;; (defrecord TreeNode [val l r])

;; ;; (TreeNode. 5 nil nil)


;; ;;;defstruct의 몰락

;; (defn change-age [p] (assoc p :age 286))

;; (defstruct person :fname :lname)
;; (change-age (struct person "Immanuel" "Kant"))

;; (defrecord Person [fname lname])
;; (change-age (Person. "Immanuel" "Kant"))

;; ;;; ex)9.1

;; (defrecord TreeNode [val l r])  ; 레코드 타입 정의

;; (defn xconj [t v]  ; 트리에 추가
;;   (cond
;;     (nil? t)       (TreeNode. v nil nil)
;;     (< v (:val t)) (TreeNode. (:val t) (xconj (:l t) v) (:r t))
;;     :else          (TreeNode. (:val t) (:l t) (xconj (:r t) v))))

;; (defn xseq [t]  ; 트리를 시퀀스(seq)로 변환
;;   (when t
;;     (concat (xseq (:l t)) [(:val t)] (xseq (:r t)))))


;; (reduce xconj nil [3 5 2 4 6])

;; (def sample-tree (reduce xconj nil [3 5 2 4 6]))  ; 테스트
;; sample-tree
;; (xseq sample-tree)

;; (dissoc (TreeNode. 5 nil nil) :l)

;; ;;;프로토콜

;; (defprotocol FIXO
;;   (fixo-push [fixo value])
;;   (fixo-pop [fixo])
;;   (fixo-peek [fixo]))


;; (extend-type TreeNode
;;   FIXO
;;   (fixo-push [node value]
;;     (xconj node value)))

;; (xseq (fixo-push sample-tree 5/2))


;; (extend-type clojure.lang.IPersistentVector
;;   FIXO
;;   (fixo-push [vector value]
;;     (conj vector value)))

;; (fixo-push [2 3 4 5 6] 5/2)


;; ;;; 클로저 스타일 믹스인 (mixin)
;; (use 'clojure.string)

;; (defprotocol StringOps (rev [s]) (upp [s]))

;; (extend-type String
;;   StringOps
;;   (rev [s] (clojure.string/reverse s)))

;; (rev "Works")

;; (extend-type String
;;   StringOps
;;   (upp [s] (clojure.string/upper-case s)))

;; (upp "Works")


;; (rev "Works?")

;; (def rev-mixin {:rev clojure.string/reverse})

;; (def upp-mixin {:upp (fn [this] (.toUpperCase this))})

;; (def fully-mixed (merge upp-mixin rev-mixin))

;; (extend String StringOps fully-mixed)

;; (-> "Works" upp rev)


;; (rev "Works?")


;; (reduce fixo-push nil [3 5 2 4 6 0])

;; (extend-type nil
;;   FIXO
;;   (fixo-push [t v]
;;     (TreeNode. v nil nil)))

;; (reduce fixo-push nil [3 5 2 4 6 0])

;; (xseq (reduce fixo-push nil [3 5 2 4 6 0]))

;; ;;;예제 9.2 TreeNode와 벡터에 대한 완전한 FIXO 구현
;; (extend-type TreeNode
;;   FIXO
;;   (fixo-push [node value]  ; xconj에 위임
;;     (xconj node value))
;;   (fixo-peek [node]  ; 왼쪽 노드로 내려가서 가장 작은 것을 찾음
;;     (if (:l node)
;;       (recur (:l node))
;;       (:val node)))
;;   (fixo-pop [node]  ; 삭제한 항목 왼쪽으로 새 경로 구성
;;     (if (:l node)
;;       (TreeNode. (:val node) (fixo-pop (:l node)) (:r node))
;;       (:r node))))

;; (extend-type clojure.lang.IPersistentVector
;;   FIXO
;;   (fixo-push [vector value]  ; fixo-push는 벡터에 conj 수행
;;     (conj vector value))
;;   (fixo-peek [vector]  ; fixo-peek는 peek 수행
;;     (peek vector))
;;   (fixo-pop [vector]  ; fixo-pop은 pop 수행
;;     (pop vector)))

;; ;;;
;; (defn fixo-into [c1 c2]
;;   (reduce fixo-push c1 c2))

;; (xseq (fixo-into (TreeNode. 5 nil nil) [2 4 6 7]))


;; (seq (fixo-into [5] [2 4 6 7]))

;; ;;;;mytest
;; (def my-Map {:key :value})
;; ;; 키가 문자열인 경우에는 키를 함수로 사용할 수 없다
;; (:key my-Map)
;; ;;;;;;;;;;;

;; (def tree-node-fixo  ; 함수와 이름의 맵핑 정의
;;   {:fixo-push (fn [node value]
;;                 (xconj node value))
;;    :fixo-peek (fn [node]
;;                 (if (:l node)
;;                   (recur (:l node))
;;                   (:val node)))
;;    :fixo-pop (fn [node]
;;                (if (:l node)
;;                  (TreeNode. (:val node) (fixo-pop (:l node)) (:r node))
;;                  (:r node)))})

;; (extend TreeNode FIXO tree-node-fixo)  ; 맵을 사용해서 프로토콜 확장

;; (xseq (fixo-into (TreeNode. 5 nil nil) [2 4 6 7]))

;; ;;;;; 예제 9.4 reify를 사용한 크기로 고정된 스택 FIXO

;; (defn fixed-fixo  ; FIXO 인스턴스를 리턴하는 팩토리
;;   ([limit] (fixed-fixo limit []))
;;   ([limit vector]
;;    (reify FIXO  ; reify는 프로토콜을 충족시키는 데 사용됨
;;      (fixo-push [this value]
;;        (if (< (count vector) limit)
;;          (fixed-fixo limit (conj vector value))
;;          this))
;;      (fixo-peek [_]
;;        (peek vector))
;;      (fixo-pop [_]
;;        (pop vector)))))

;; ;;;;;(defn fixed-fixo  ; FIXO 인스턴스를 리턴하는 팩토리
;;   ([limit] (fixed-fixo limit []))
;;   ([limit vector]
;;    (reify FIXO  ; reify는 프로토콜을 충족시키는 데 사용됨
;;      (fixo-push [this value]
;;        (if (< (count vector) limit)
;;          (fixed-fixo limit (conj vector value))
;;          this))
;;      (fixo-peek [_]
;;        (peek vector))
;;      (fixo-pop [_]
;;        (pop vector)))))

;; ;;;;; **예제 9.5 defrecord 안에서 메서드 구현하기**

;; (defrecord TreeNode [val l r]
;;   FIXO   ; FIXO 메서드들을 인라인으로 구현
;;   (fixo-push [t v]
;;              (if (< v val)
;;                (TreeNode. val (fixo-push l v) r)
;;                (TreeNode. val l (fixo-push r v))))

;;   (fixo-peek [t]
;;              (if l
;;                (fixo-peek l)  ; recur 대신 메서드를 호출
;;                val))
;;   (fixo-pop [t]
;;             (if l
;;               (TreeNode. val (fixo-pop l) r)
;;               r)))

;; (def sample-tree2 (reduce fixo-push (TreeNode. 3 nil nil) [5 2 4 6]))
;; (xseq sample-tree2)

;; ;;;;;9.3.3 deftype으로 밑바닥부터 구현하기

;; (defrecord InfiniteConstant [i]
;;   clojure.lang.ISeq
;;   (seq [this]
;;        (lazy-seq (cons i (seq this)))))

;; (deftype InfiniteConstant [i]
;;   clojure.lang.ISeq
;;   (seq [this]
;;     (lazy-seq (cons i (seq this)))))

;; (take 3 (InfiniteConstant. 5))

;; (:i (InfiniteConstant. 5))

;; (.i (InfiniteConstant. 5))

;; ;;;;; 예제 9.6 deftype으로 맵 인터페이스 구현하기

;; (deftype TreeNode [val l r]
;;   FIXO       ; FIXO 메서드들을 인라인으로 구현
;;   (fixo-push [_ v]
;;              (if (< v val)
;;                (TreeNode. val (fixo-push l v) r)
;;                (TreeNode. val l (fixo-push r v))))
;;   (fixo-peek [_]
;;              (if l
;;                (fixo-peek l)  ; recur 사용 대신 메서드를 호출
;;                val))
;;   (fixo-pop [_]
;;             (if l
;;               (TreeNode. val (fixo-pop l) r)
;;               r))
  
;;   clojure.lang.IPersistentStack  ; 인터페이스 구현
;;   (cons [this v] (fixo-push this v))
;;   (peek [this] (fixo-peek this))
;;   (pop [this] (fixo-pop this))
  
;;   clojure.lang.Seqable
;;   (seq [t]
;;        (concat (seq l) [val] (seq r))))

;; (extend-type nil
;;   FIXO
;;   (fixo-push [t v]
;;     (TreeNode. v nil nil)))  ; 새 TreeNode 사용을 위한 재정의

;; (def sample-tree2 (into (TreeNode. 3 nil nil) [5 2 4 6]))
;; (seq sample-tree2)