;; (ns joy.ch6-2
;;   (:gen-class)
;;   (:require [clojure.string :as str-]
;;             [clojure.test :as t]))

;; (def baselist (list :barnabas :adam))
;; (def lst1 (cons :willie baselist))
;; (def lst2 (cons :phoenix baselist))

;; lst1
;; lst2

;; (= (next lst1) (next lst2))

;; (identical? (next lst1) (next lst2))


;; (defn xconj [t v]
;;   (cond
;;     (nil? t) {:val v, :L nil, :R nil} ;; 노드가 nil이면 v로 시작
;;     (< v (:val t)) {:val (:val t), ;; v가 현재 노드보다 작으면 왼쪽에 추가
;;                     :L (xconj (:L t) v),
;;                     :R (:R t)}
;;     :else {:val (:val t), ;; 크거나 같으면 오른쪽에 추가
;;            :L (:L t),
;;            :R (xconj (:R t) v)}))


;; ;; (defn xconj [t v] ;; 트리(t)에 값(v)를 추가하는 함수
;; ;;   (cond
;; ;;     (nil? t) {:val v, :L nil, :R nil}))

;; ;; (xconj nil 5)

;; ;;;;;;;;;;;;;;;;;

;; ;; (defn xconj [t v]
;; ;;   (cond
;; ;;     (nil? t) {:val v, :L nil, :R nil}
;; ;;     (< v (:val t)) {:val (:val t),
;; ;;                     :L (xconj (:L t) v),
;; ;;                     :R (:R t)}))

;; (def tree1 (xconj nil 5))
;; tree1


;; (def tree1 (xconj tree1 3))
;; tree1


;; (def tree1 (xconj tree1 2))
;; tree1

;; {:val 5, :L nil, :R nil}

;; (defn xseq [t]
;;   (when t
;;     (concat (xseq (:L t)) [(:val t)] (xseq (:R t)))))


;; (xseq tree1)

;; (def tree2 (xconj tree1 7))
;; (xseq tree2)


;; (identical? (:L tree1) (:L tree2))