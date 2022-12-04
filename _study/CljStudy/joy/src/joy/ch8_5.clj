(ns joy.ch8-5)

(defmacro resolution [] `x)

(macroexpand '(resolution))

(def x 9)
(let [x 109] (resolution))


(defmacro awhen [expr & body]
  `(let [~'it ~expr]  ; 대용어 정의
     (if ~'it  ; 참인지 확인
       (do ~@body))))  ; body 인라인 평가

(awhen [1 2 3] (it 2))


(awhen nil (println) "Will never get here")


(awhen 1 (awhen 2 [it]))