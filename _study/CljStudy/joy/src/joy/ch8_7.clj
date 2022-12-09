(ns joy.ch8-7)

(contract doubler
          [x]
          (:require
           (pos? x))
          (:ensure
           (= (* 2 x) %)))

(declare collect-bodies)

(defn build-contract [c]
  (let [args (first c)]
    (list
     (into '[f] args)
     (apply merge
            (for [con (rest c)]
              (cond (= (first con) 'require)
                    (assoc {} :pre (vec (rest con)))
                    (= (first con) 'ensure)
                    (assoc {} :post (vec (rest con)))
                    :else (throw (Exception.,
                                  (str "Unknown tag "
                                       (first con)))))))
     (list* 'f args))))

(defn collect-bodies [forms]
  (for [form (partition 3 forms)]
    (build-contract form)))

(defmacro contract [name & forms]
  (list* `fn name (collect-bodies forms)))

(fn doubler 
  ([f x]
   {:post [(= (* 2 x) %)],
    :pre [(pos? x)]}
   (f x)))