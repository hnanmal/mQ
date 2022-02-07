(ns webapp.core
  (:import [org.eclipse.jetty.server Server ServerConnector]
           [org.eclipse.jetty.server.handler.AbstractHandler]))

(def handler
  (proxy [AbstractHandler] []
    (handle [target base-request request ^HttpServletResponse response]
      (with-open [writer (.getWriter response)]
        (.print writer "Hello World")))))

(defn -main [& args]
  (let [^Server server (Server.)
        ^ServerConnector connector (doto (ServerConnector. server)
                                     (.setPort 8080))]
    (doto server
      (.addConnector connector)
      (.setHandler handler)
      (.start)
      (.join))))