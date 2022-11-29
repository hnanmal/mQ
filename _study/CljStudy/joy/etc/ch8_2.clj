;; (ns joy.ch8-2 
;;   (:require [clojure.walk :as walk]))

;; (defmacro do-until [& clauses]
;;   (when clauses
;;     (list 'clojure.core/when (first clauses)
;;           (if (next clauses)
;;             (second clauses)
;;             (throw (IllegalArgumentException.
;;                     "do-until requires an even number of forms")))
;;           (cons 'do-until (nnext clauses)))))


;; (do-until
;;  (even? 2) (println "Even")
;;  (odd? 3) (println "Odd")
;;  (zero? 1) (println "You never see me")
;;  :lollipop (println "Truthy thing"))

;; ; Even
;; ; Odd
;; ;=> nil

;; (macroexpand-1 '(do-until true (prn 1) false (prn 2)))

;; (require '[clojure.walk :as walk])
;; (walk/macroexpand-all '(do-until true (prn 1) false (prn 2)))

;; (do-until true (prn 1) false (prn 2))

;; (defmacro unless [condition & body]
;;   `(if (not ~condition)
;;      (do ~@body)))

;; (unless (even? 3) "Now we wee it...")


;; (unless (even? 2) "Now we don't.")


;; (unless true (println "nope"))


;; (unless false (println "yep!"))


;; (macroexpand `(if (not condition) "got it"))

;; (eval `(if (not condition) "got it"))

;; (def condition false)
;; (eval `(if (not condition) "got it"))