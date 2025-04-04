;; (ns joy.ch9-4)

;; (defn build-move [& pieces]
;;   (apply hash-map pieces))

;; (build-move :from "e7" :to "e8", :promotion \Q)

;; ;;;;; 레코드 사용

;; (defrecord Move [from to castle? promotion]
;;  Object
;;   (toString [this]
;;             (str "Move " (:from this)
;;                  " to " (:to this)
;;                  (if (:castle? this)
;;                    " castle"
;;                    (if-let [p (:promotion this)]
;;                      (str " promote to " p)
;;                      "")))))

;; ;; (defrecord Move [from to castle? promotion]
;; ;;   Object
;; ;;   (toString [this]
;; ;;     (str "Move " (:from this)
;; ;;          " to " (:to this)
;; ;;          (if (:castle? this)
;; ;;            " castle"))))

;; (str (Move. "e2" "e4" nil nil))
;; (str (Move. "e2" "e4" "dd" \Q))

;; (.println System/out (Move. "e7" "e8" nil \Q))


;; ;;;;; 관심사의 분리

;; (defn build-move [& {:keys [from to castle? promotion]}]
;;   {:pre [from to]}
;;   (Move. from to castle? promotion))

;; (str (build-move :from "e2" :to "e4"))