(ns joy.ch7-3)

(defn pow [base exp]
  (if (zero? exp)
    1
    (* base (pow base (dec exp)))))

(pow 2 10)


(pow 1.01 925)


(pow 2 10000)


(defn pow [base exp]
  (letfn [(kapow [base exp acc]
                 (if (zero? exp)
                   acc
                   (recur base (dec exp) (* base acc))))]
    (kapow base exp 1)))

(pow 2N 10000)