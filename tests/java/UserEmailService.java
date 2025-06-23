public class UserEmailService {
    // SHOULD FAIL: Hardcoded email in constant
    private static final String EMAIL = "test@example.com";

    // SHOULD NOT FAIL: Not an email address
    private static final String NOT_EMAIL = "test-at-example.com";

    // SHOULD FAIL: Email in string literal
    public void test1() {
        System.out.println("Contact admin@example.com");
    }

    // SHOULD NOT FAIL: Email as parameter
    public void test2(String userEmail) {
        System.out.println(userEmail);
    }
}