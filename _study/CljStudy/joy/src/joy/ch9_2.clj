(ns joy.udp
  (:refer-clojure :exclude [get]))  ; clojure.core/get을 참조에서 제외


(defn beget [this proto]
  (assoc this ::prototype proto))  ; 맵을 받아서 :joy.udp/prototype 키에 프로토타입을 연결한다.


(beget {:sub 0} {:super 1})


(defn get [m k]
  (when m
    (if-let [[_ v] (find m k)]
      v
      (recur (::prototype m) k))))

(get (beget {:sub 0} {:super 1})
     :super)


(def put assoc)


;;;;

(def cat {:likes-dogs true, :ocd-bathing true})
(def morris (beget {:likes-9lives true} cat))
(def post-traumatic-morris (beget {:likes-dogs nil} morris))

(get cat :likes-dogs)


(get morris :likes-dogs)

post-traumatic-morris

(get post-traumatic-morris :likes-dogs)


(get post-traumatic-morris :likes-9lives)


;;;;;

(defmulti compiler :os)
(defmethod compiler ::unix [m] (get m :c-compiler))
(defmethod compiler ::osx [m] (get m :llvm-compiler))

(def clone (partial beget {}))
(def unix {:os ::unix, :c-compiler "cc", :home "/home", :dev "/dev"})
(def osx (-> (clone unix)
             (put :os ::osx)
             (put :llvm-compiler "clang")
             (put :home "/Users")))

(compiler unix)


(compiler osx)

unix
osx

(defmulti home :os)
(defmethod home ::unix [m] (get m :home))

(home unix)


(home osx)

(derive ::osx ::unix)


(home osx)
;;

(parents ::osx)


(ancestors ::osx)


(descendants ::unix)


(isa? ::osx ::unix)


(isa? ::unix ::osx)


;;;계층 모순
(derive ::osx ::bsd)
(defmethod home ::bsd [m] "/home")

(home osx)

(prefer-method home ::unix ::bsd)
(home osx)


(remove-method home ::bsd)
(home osx)


(derive (make-hierarchy) ::osx ::unix)


;;;임의적 디스패치 힘

(defmulti compile-cmd (juxt :os compiler))  ; juxt는 벡터를 구성함

(defmethod compile-cmd [::osx "gcc"] [m]  ; 벡터를 정확하게 매치시킴
 (str "/user/bin/" (get m :c-compiler)))

(defmethod compile-cmd :default [m]
  (str "Unsure where to locate " (get m :c-compiler)))


(compile-cmd osx)


(compile-cmd unix)