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
