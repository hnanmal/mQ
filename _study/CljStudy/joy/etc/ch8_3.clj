;; (ns joy.ch8-3)

;; (defmacro def-watched [name & value]
;;   `(do
;;      (def ~name ~@value)
;;      (add-watch (var ~name)
;;                 :re-bind
;;                 (fn [~'key ~'r old# new#]
;;                   (println old# " -> " new#)))))

;; ;; (do (def x 2)
;; ;;     (add-watch (var x)
;; ;;                :re-bind
;; ;;                (fn [key r old new]
;; ;;                  (println old# " -> " new#))))

;; (def-watched x (* 12 12))

;; (def x 0)