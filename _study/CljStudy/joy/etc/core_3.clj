;; (ns joy.core
;;   (:gen-class))


;; :a-keyword
;; ::also-a-keyword

;; (defn pour [lb ub]
;;   (cond
;;     (= ub :toujours) (iterate inc lb)
;;     :else (range lb ub)))

;; (pour 1 10)

;; (pour 1 :toujours)

;; ::not-in-ns
;; :not-in-ns

;; (identical? 'goat 'goat)
;; (= 'goat 'goat)
;; (name 'goat)

;; (let [x 'goat, y x]
;;   (identical? x y))

;; (let [x (with-meta 'goat {:ornery true})
;;       y (with-meta 'goat {:ornery false})]
;;   [(= x y)
;;    (identical? x y)
;;    (meta x)
;;    (meta y)])

;; (defn best [f xs]
;;   (reduce #(if (f % %2) % %2) xs))

;; (best > [1 3 4 2 7 5 3])
;; (best < [1 3 4 2 7 5 3])

;; #"an example pattern"

;; (class #"example")
;; (java.util.regex.Pattern/compile "\\d")

;; (re-seq #"\w+" "one-two/three")

;; ;; 이 예제는 영속적 데이터구조를 사용한 경우와 자바 배열을
;; ;; 사용하여 영속적 데이터구조가 아닌 경우를 비교하고 있다.
;; (def ds (into-array [:willie :barnabas :adam]))
;; (seq ds)

;; ;; 이 예제는 키워드 배열의 세 항목을 생성하고, seq를 사용해서
;; ;; 객체를 만들어 REPL 상에 보여준다. 배열 ds의 변화가 발생하면
;; ;; 그 전에 입력한 내용은 모두 사라져 버린다.

;; (aset ds 1 :quentin)
;; ds
;; (seq ds)

;; (def ds [:willie :barnabas :adam])
;; ds
;; (def ds1 (replace {:barnabas :quentin} ds))
;; ds
;; ds1


;; ;; 순차적 컬렉션은 일련의 값들을 재정렬하지 않고 그대로 저장한다.
;; ;; 일반적으로 셋, 맵과 함께 널리 사용되는 세가지 컬렉션 타입의 종류 중 하나다.

;; ;; 시퀀스(sequence)는 존재하거나 아직 존재하지 않을 수도 있는
;; ;; 일련의 값들을 표현하는 순차적 컬렉션이다.
;; ;; 이 값들은 실제하는 컬렉션으로부터 올 수도 있고
;; ;; 필요에 따라 계산된 결과일 수도 있다.
;; ;; 또 시퀀스는 비어있을 수도 있다.

;; ;; 클로저는 시퀀스(seq)라고 불리는 컬렉션을 탐색하는 데
;; ;; 사용되는 단순한 API를 갖고 있다.
;; ;; seq는 first 와 rest 함수를 갖는다.
;; ;; 컬렉션에 뭔가 들어 있으면 (first coll)은 그 첫번째 항목을
;; ;; 리턴하고, 아무것도 없으면 nill을 리턴한다.
;; ;; (rest coll)은 첫 번째 항목을 제외한
;; ;; 나머지 항목들의 시퀀스를 리턴한다.

;; ;; 동일성 구획
;; (= [1 2 3] '(1 2 3))

;; (= [1 2 3] #{1 2 3})

;; ;; 시퀀스 추상화
;; ;; 많은 리습 계열 언어들은 cons 셀 추상화를 기반으로
;; ;; 각자의 데이터 타입을 만든다.
;; ;; Cons 셀 추상화는 그림 5.1과 같이 두 항목 간의 연결구조로
;; ;; 표현할 수 있다. Cons 셀은 자바 코어 라이브러리의
;; ;; java.util.LinkedList 타입과 유사한 링크드 리스트 구조로 이루어져 있다.

;; ;; ...클로저도 cons 셀 쌍과 유사한 구조를 갖고 있다.
;; ;; 이에 대해서는 5.4절에서 알아볼 것이지만, 이것이 클로저 설계의
;; ;; 근간을 이루고 있지는 않다.
;; ;; 그 대신 cons 셀에 의해 만들어진 개념적 인터페이스가 앞서
;; ;; 설명했던 시퀀스라 불리는 실제적인 구조를 뒷받침하고 있다.
;; ;; 이 구조의 핵심적인 두 함수 first 와 rest를 지원하려면
;; ;; 모든 객체가 시퀀스일 필요가 있다.
;; ;; 그러나 filter, map, for, doseq, take, partition
;; ;; 그 외에도 수많은 클로저가 제공하는 강력한 시퀀스 함수
;; ;; 라이브러리와 컬렉션에 사용가능한 매크로 등이 제공되는 것을
;; ;; 생각하면 그리 과한 조건은 아니다.
;; ;; 이와 동시에 많은 객체들이 이 인터페이스를 이미 따르고 있다.
;; ;; 모든 클로저 컬렉션들은 그 항목들을 탐색하기 위한 시퀀스(seq)
;; ;; 객체를 적어도 하나는 제공하고 있고,
;; ;; 이를 seq 함수를 통해 노출시킨다.
;; ;; 어떤 컬렉션은 한 개 이상을 제공하기도 한다.
;; ;; 예를 들어 벡터는 rseq를 지원하고, 맵은 keys와 vals를 제공한다

;; (def 어떤벡터 [1 2 3 4 5])
;; (seq 어떤벡터)
;; (rseq 어떤벡터)
;; (def someMap {:name "qooqoo" :cost 3000})
;; (seq someMap)
;; (keys someMap)
;; (vals someMap)

;; (class (hash-map :a 1))
;; (seq (hash-map :a 1))
;; (class (seq (hash-map :a 1)))
;; (seq (keys (hash-map :a 1)))
;; (class (keys (hash-map :a 1)))
;; (range 10)
;; (vec (range 10))
;; (let [my-vector [:a :b :c]]
;;   (into my-vector (range 10))
;;   my-vector)

;; (into (vector-of :int) [Math/PI 2 1.3])
;; (into (vector-of :char) [100 101 102])
;; ;; (into (vector-of :long) [1 2 617281728182918291289121862])

;; ;; 컬렉션의 크기가 작을 때는 벡터와
;; ;; 리스트 간의 성능 차이가 거의 나지 않지만 둘의 크기가 커지면
;; ;; 한 쪽은 효율적으로 동작하는 반면 다른 한 쪽은 극적으로
;; ;; 느려지게 된다. 특히 컬렉션의 오른쪽 끝에 항목을 추가/삭제하는
;; ;; 경우와 숫자 인덱스로 컬렉션 내부 항목에 접근하거나 변경하는
;; ;; 경우, 그리고 역순으로 조회하는 이 세가지 경우에는 리스트에
;; ;; 비해 효율적으로 동작한다. 끝부분에 항목을 추가하거나 삭제하는
;; ;; 것은 벡터를 스택으로 취급하면 되는데, 5.2.3절에서 설명할 것이다.

;; (def a-to-j (vec (map char (range 65 75))))
;; a-to-j
;; (nth a-to-j 4)
;; (get a-to-j 4)
;; (a-to-j 4)

;; (seq a-to-j)
;; (rseq a-to-j)
;; (assoc a-to-j 4 "no longer E")
;; (replace {2 :a 4 :b} [1 2 3 2 3 4])

;; (def matrix
;;   [[1 2 3]
;;    [4 5 6]
;;    [7 8 9]])

;; (get-in matrix [1 2])
;; (assoc-in matrix [1 2] ':x)
;; (update-in matrix [1 2] * 100)

;; 예제 5.1: 2차원 행렬의 특정 좌표에 대한 이웃을 찾는 함수
;; (defn neighbors
;;   ([size yx] (neighbors [[-1 0] [1 0] [0 -1] [0 1]]
;;                         size
;;                         yx))
;;   ([deltas size yx]
;;    (filter (fn [new-yx]
;;              (every? #(< -1 % size) new-yx))
;;            (map #(vec (map + yx %))
;;                 deltas))))

;; (neighbors 3 [0 0])
;; (neighbors 3 [1 1])

;; ;; 5.2.3 스택으로서의 벡터
;; ;; 전통적인 스택은 최소한 push, pop 두 가지 동작을 포함한다.
;; ;; 클로저의 벡터에서는 각각 conj와 pop으로 불린다.
;; ;; conj 함수는 벡터에 항목을 추가하고, pop은 벡터로부터 항목을
;; ;; 제거하며, 이러한 동작들은 스택의 오른쪽에서 이루어진다.
;; ;; 벡터의 값은 변경할 수 없기 때문에 pop은 오른쪽 끝에 있는 값을
;; ;; 제외한 새로운 벡터를 리턴하는데, 값 변경이 가능한 다른
;; ;; 스택 API들이 일반적으로 대상 항목을 제거하고 리턴하는 것과
;; ;; 다른 점이다. 따라서 스택의 최상단으로부터 항목을 얻을 수 있는
;; ;; 방법으로써 peek의 역할이 더 중요해지게 된다.
;; (def my-stack [1 2 3])
;; (peek my-stack)
;; (pop my-stack)
;; (conj my-stack 4)
;; (+ (peek my-stack) (peek (pop my-stack)))







;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args])
