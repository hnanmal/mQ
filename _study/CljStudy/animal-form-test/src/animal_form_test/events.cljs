(ns animal-form-test.events
  (:require
   [re-frame.core :as rf]
   [animal-form-test.db :as db]
   [day8.re-frame.tracing :refer-macros [fn-traced]]
   ))

(rf/reg-event-db  ; (reg-event-db id handler) or (reg-event-db id interceptors handler)
 ::initialize-db
 (fn-traced [_ _]
   db/default-db))

(rf/reg-event-db
 ::update-form 
 (fn [db [_ id val]]
   (assoc-in db [:form id] val)))  ; db 맵에 :form 이라는 키워드 하위에 id 라는 값 넣고, 거기에 val 값을 넣어준다
                                   ; view파일에서 [text-input :animal-name]텍스트 인풋 부분의 :animal-name 이 id 값이다.
; 즉 view file에서 텍스트 인풋이 있으면, 전체 db의 form이라는 키를 찾고(없으면 생성한 뒤) 해당 인풋객체의 id값으로 또다시 키를 생성하고, 그 키에 텍스트 인풋에 채워진 사용자 입력값을 저장한다.
;(모든 html 객체에는 id를 부여해서 관리할 수 있는 것 같다.)

;; (assoc-in {} [:key1 :key2] "val")


(rf/reg-event-db
 ::save-form
 (fn [db]
   (let [form-data (get db :form)
         animals (get db :animals [])
         updated-animals (conj animals form-data)]
     (-> db
         (assoc :animals updated-animals)
         (dissoc :form)))))