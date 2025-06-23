# Ruby test file with privacy violations
user_email = "test@example.com"
user_ssn = "123-45-6789"
user_phone = "555-123-4567"

def process_user_data(user)
  puts "Processing user: #{user[:email]}" # PII in console log
  {
    id: user[:id],
    email: user[:email],
    ssn: user[:ssn] # Sensitive data
  }
end

api_key = "sk-1234567890abcdef" # API key
user_data = {
  name: "John Doe",
  email: "john@example.com",
  phone: "555-987-6543",
  address: "123 Main Street, Anytown, CA 90210"
} 