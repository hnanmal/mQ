(ns joy.ch9-1)

;; user=> (in-ns 'joy.ns)  ; 네임스페이스 생성 및 전환
;; #object[clojure.lang.Namespace 0x3441c2ad "joy.ns"]

;; joy.ns=> (def authors ["Chouser"])
;; #'joy.ns/authors

;; joy.ns=> (in-ns 'your.ns)  ; 다른 네임스페이스 생성
;; #object[clojure.lang.Namespace 0x3061fa78 "your.ns"]

;; your.ns=> (clojure.core/refer 'joy.ns)  ; 다른 네임스페이스의 모든 정의를 가져옴
;; nil

;; your.ns=> joy.ns/authors
;; ["Chouser"]

;; your.ns=> (in-ns 'joy.ns)  ; 네임스페이스 전환
;; #object[clojure.lang.Namespace 0x3441c2ad "joy.ns"]

;; joy.ns=> (def authors ["Chouser" "Fogus"])
;; #'joy.ns/authors

;; joy.ns=> (in-ns 'your.ns)  ; 다시 돌아와서, 다른 네임스페이스의 값 재확인
;; #object[clojure.lang.Namespace 0x3061fa78 "your.ns"]

;; your.ns=> joy.ns/authors
;; ["Chouser" "Fogus"]

(ns chimp)
(reduce + [1 2 (Integer. 3)])


(in-ns 'gibbon)

(reduce + [1 2 (Integer. 3)])


(def b (create-ns 'bonobo))
b

((ns-map b) 'String)


(intern b 'x 9)

bonobo/x


(intern b 'reduce clojure.core/reduce)


(intern b '+ clojure.core/+)


(in-ns 'bonobo)
(reduce + [1 2 3 4 5])


(in-ns 'user)

(get (ns-map 'bonobo) 'reduce)


(ns-unmap 'bonobo 'reduce)


(get (ns-map 'bonobo) 'reduce)


(remove-ns 'bonobo)

(all-ns)


;;;;
(create-ns 'hider.ns)
(ns hider.ns)

(defn ^{:private true} answer [] 42)


(ns seeker.ns
  (:refer hider.ns))

(answer)