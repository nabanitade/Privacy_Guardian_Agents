// C# test file with privacy violations
using System;

public class UserService
{
    private string userEmail = "test@example.com";
    private string userSSN = "123-45-6789";
    private string userPhone = "555-123-4567";
    
    public void ProcessUserData(User user)
    {
        Console.WriteLine($"Processing user: {user.Email}"); // PII in console log
        var userData = new
        {
            Id = user.Id,
            Email = user.Email,
            SSN = user.SSN // Sensitive data
        };
    }
    
    private string apiKey = "sk-1234567890abcdef"; // API key
    
    public class User
    {
        public string Name { get; set; } = "John Doe";
        public string Email { get; set; } = "john@example.com";
        public string Phone { get; set; } = "555-987-6543";
        public string Address { get; set; } = "123 Main Street, Anytown, CA 90210";
        public string SSN { get; set; } = "987-65-4321";
    }
} 