(ns joy.ch8-1)

(->
 (/ 144 12)
 (/ 2 3)
 str
 keyword
 list)

(->
 (/ 144 12)
 (* 4 (/ 2 3))
 str
 keyword
 (list :33))

(eval 42)


(eval '(list 1 2))


(eval (list 1 2))


(eval (list (symbol "+") 1 2))


(defn contextual-eval [ctx expr]
  (eval
   `(let [~@(mapcat (fn [[k v]] [k `'~v]) ctx)]
      ~expr)))

(contextual-eval '{a 1, b 2} '(+ a b))


(contextual-eval '{a 1, b 2} '(let [b 1000] (+ a b)))