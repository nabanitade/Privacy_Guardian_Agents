// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

public class PrivacyTest {
    
    // PII Detection Rule violations
    private String ssn = "123-45-6789";
    private String creditCard = "4111-1111-1111-1111";
    private String phone = "555-123-4567";
    private String address = "123 Main Street, Anytown, CA 90210";
    
    // Privacy Policy Rule violations
    public void deleteUserData() {
        // GDPR violation - hardcoded user deletion
        String query = "delete from users where id = 12345";
        // CCPA violation - selling user data
        boolean sellUserData = true;
        // Data minimization violation
        String collectAllData = "collect all user information";
    }
    
    // AI Privacy Rule violations
    public void logUserInfo() {
        // PII in logs violation
        System.out.println("User email: " + userEmail);
        logger.info("Customer phone: " + customerPhone);
    }
    
    // Developer Guidance Rule violations
    public void createUser() {
        // Object creation with PII
        User user = new User("John Doe", "john@example.com", "555-123-4567");
        // Data storage operation
        saveUserData(user);
    }
    
    private void saveUserData(User user) {
        // This would trigger multiple privacy violations
        database.insert("users", user);
    }
} 