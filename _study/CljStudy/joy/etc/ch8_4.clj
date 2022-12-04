;; (ns joy.ch8-4)

;; (defmacro domain [name & body]
;;   `{:tag :domain,
;;    :attrs {:name (str '~name)},
;;    :content [~@body]})

;; (declare handle-things)

;; (defmacro grouping [name & body]
;;   `{:tag :grouping,
;;     :attrs {:name (str '~name)}
;;     :content [~@(handle-things body)]})

;; (declare grok-attrs grok-props)

;; (defn handle-things [things]
;;   (for [t things]
;;     {:tag :things,
;;      :attrs (grok-attrs (take-while (comp not vector?) t))
;;      :content (if-let [c (grok-props (drop-while (comp not vector?) t))]
;;                 [c]
;;                 [])}))

;; (defn grok-attrs [attrs]
;;   (into {:name (str (first attrs))}
;;         (for [a (rest attrs)]
;;           (cond
;;             (list? a) [:isa (str (second a))]
;;             (string? a) [:comment a]))))

;; (defn grok-props [props]
;;   (when props
;;     {:tag :properties, :attrs nil,
;;      :content (apply vector (for [p props]
;;                               {:tag :property,
;;                                :attrs {:name (str (first p))},
;;                                :content nil}))}))

;; (def d
;;   (domain man-vs-monster
;;           (grouping people  ; 인간 그룹
;;                     (Human "A stock human")  ; 한 종류의 사람
                    
;;                     (Man (isa Human)  ; 다른 종류의 사람
;;                          "A man, baby"
;;                          [name]
;;                          [has-beard?]))
;;           (grouping monsters  ; 괴물 그룹
;;                     (Chupacabra  ; 한 종류의 괴물
;;                      "A fierce, yet elusive creature"
;;                      [eats-goats?]))))


;; (:tag d)


;; (:tag (first (:content d)))


;; (use '[clojure.xml :as xml])
;; (xml/emit d)