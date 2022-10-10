(ns joy.ch7-1)

(map
 [:chthon :phthor :beowulf :grendel]
 #{0 3})

(map
 [:chthon :phthor :beowulf :grendel]
 [0 3])

(map
 [:chthon :phthor :beowulf :grendel]
 '(0 3))

;;;
(def fifth (comp first rest rest rest rest))
(fifth [1 2 3 4 5])

(defn fnth [n]
  (apply comp
         (cons first
               (take (dec n) (repeat rest)))))

((fnth 5) '[a b c d e])

(cons first
      (take (dec 4) (repeat rest)))

(apply comp
       (cons first
             (take (dec 4) (repeat rest))))

(map (comp  ; 함수 구성
      keyword  ; 키워드 생성
      #(.toLowerCase %)  ; 소문자로 변환
      name)  ; 이름을 string으로 리턴
     '(a B C))  ; 합성한 함수를 심벌의 리스트에 맵핑

;;;
((partial + 5) 100 200)

