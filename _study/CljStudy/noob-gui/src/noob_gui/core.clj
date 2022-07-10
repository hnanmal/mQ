(ns noob-gui.core
  (:gen-class))

(import '(javax.swing JFrame JPanel JButton))
(def button (JButton. "Click Me!"))
(def panel (doto (JPanel.)
             (.add button)))
(def frame (doto (JFrame. "Hello Frame")
             (.setSize 200 200)
             (.setContentPane panel)
             (.setVisible true)))

(import 'javax.swing.JOptionPane)
(defn say-hello []
  (JOptionPane/showMessageDialog
   nil "Hello, World!" "Greeting"
   JOptionPane/INFORMATION_MESSAGE))

(import 'java.awt.event.ActionListener)
(def act (proxy [ActionListener] []
           (actionPerformed [event] (say-hello))))

(.addActionListener button act)

;; 기본적인 스윙 래핑 예제
(import '(javax.swing JFrame JTable JScrollPane))
(import '(javax.swing.table DefaultTableModel))

(let
 [frame (JFrame. "Hello Swing")
  dm (DefaultTableModel.)
  table (JTable. dm)
  scroll (JScrollPane. table)]
  (doto dm
    (.setNumRows 30)
    (.setColumnCount 5))
  (.. frame getContentPane (add scroll))
  (doto frame
    (.setDefaultCloseOperation JFrame/EXIT_ON_CLOSE)
    (.pack)
    (.setVisible true)))


(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))
