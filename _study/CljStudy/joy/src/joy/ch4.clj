(ns joy.ch4)

1.0E-430000000M

1.0E-4300000000M


:a-keyword

:also-a-keyword



(defn pour [lb ub]
  (cond
    (= ub :toujours) (iterate inc lb)
    :else (range lb ub)))

(pour 1 10)

(pour 1 :toujours)

::not-in-ns

(ns another)

(defn do-blowfish [directive]
  (case directive
    :aquarium/blowfish (println "feed the fish")
    :crypto/blowfish   (println "encode the message")
    :blowfish          (println "not sure what to do")))
(ns crypto)
(do-blowfish :blowfish)


(user/do)