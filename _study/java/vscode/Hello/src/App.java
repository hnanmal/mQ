public class App {
    public static void main(String[] args) throws Exception {
        java.util.HashMap props = new java.util.HashMap<>();
        props.put("HOME", "home/me");    /* 일부 코드 생략 */
        props.put("SRC", "src");
        props.put("BIN", "classes");
        System.out.println(props);
    }
}
