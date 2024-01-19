; (import numpy [:as np])
; (import [functools [partial reduce]])

; (import numpy)

(print "hy hi")

(print "hello world")

(defn something-fancy [wow &rest descriptions &kwargs props]
  (print "Look at" wow)
  (print "It's" descriptions)
  (print "And it also has:" props))

(for [x [1 2 3]]
  (print x))