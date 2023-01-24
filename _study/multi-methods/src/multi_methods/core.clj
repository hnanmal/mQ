(ns multi-methods.core)

(+ 1 1)

(def user1 {:name "mark" :contact-method "sms"})
(def user2 {:name "Tom" :contact-method "phone"})
(def user3 {:name "Travis" :contact-method "email"})
(def user4 {:name "Matt"})


;; (defn sms-user [user] (str "Sending SMS to " (:name user)))
;; (defn email-user [user] (str "Sending email to " (:name user)))
;; (defn phone-user [user] (str "Phoning " (:name user)))

;; (defn dispatch-notify-function [user] (:contact-method user))
  

(defmulti notify-user :contact-method)
(defmethod notify-user "sms" [user] 
  (str "Sending SMS to " (:name user)))
(defmethod notify-user "phone" [user] 
  (str "Phoning " (:name user)))
(defmethod notify-user :default [user] 
  (str "Sending email to " (:name user)))
 

(notify-user user1)
(notify-user user2)
(notify-user user3)
(notify-user user4)
