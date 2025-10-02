// ExtendC Language Comprehensive Test Cases
// Testing all lexical analyzer features

/* 
   Multi-line comment
   Testing multi-line comment detection
*/

// 1. Testing Keywords - Standard C Keywords
int main() {
    auto char const continue default do double else enum extern 
    float for goto if long register return short signed sizeof 
    static struct switch typedef union unsigned void volatile while
    break case
}

// 2. Testing New ExtendC Keywords
phone phoneVar;
email emailVar;

// 3. Testing Identifiers
int variable1;
float _privateVar;
char userName123;
int _valid_identifier;

// 4. Testing Integer Constants
int num1 = 0;
int num2 = 123;
int num3 = 999999;

// 5. Testing Float Constants
float pi = 3.14;
float rate = 0.05;
float large = 999.999;

// 6. Testing String Constants
char* message = "Hello World";
char* path = "C:\\Users\\Documents\\file.txt";
char* escaped = "Line1\nLine2\tTabbed";
char* quote = "He said \"Hello\"";

// 7. Testing Character Constants  
char ch1 = 'A';
char ch2 = '5';
char ch3 = '\n';
char ch4 = '\'';
char ch5 = '\\';

// 8. Testing Phone Number Patterns
phone p1 = 9876543210;          // 10 digits
phone p2 = +91-9876543210;      // With country code
phone p3 = 1234567890;          // Another valid 10-digit

// 9. Testing Email Address Patterns
email e1 = user@example.com;
email e2 = first.last@domain.co.in;
email e3 = test123@gmail.com;
email e4 = admin_user@company.org;
email e5 = contact+info@website.net;

// 10. Testing All Operators
int a = 5;
int b = 10;
if (a == b) a++;
if (a != b) b--;
if (a < b) a = a + b;
if (a > b) a = a - b;
if (a <= b) a = a * b;
if (a >= b) a = a / b;

// 11. Testing All Punctuators
{
    int arr[5];
    func(a, b, c);
    statement1;
    statement2;
}

// 12. Testing Comments in Different Positions
int x = 5; // End of line comment
// Comment at beginning of line
/* Inline comment */ int y = 10;

/*
Multi-line comment
with multiple lines
and various content: symbols @#$%^&*()
*/

// 13. Testing Mixed Complex Expressions
if ((x + y) >= (a * b)) {
    phone contact = +91-9999888877;
    email notify = admin@system.com;
    char msg = 'Y';
    float result = 123.456;
}

// 14. Testing Edge Cases
char empty = '';            // This should cause an error
int negative = -123;        // Testing negative numbers
float scientific = 1.5e10; // This might not be supported
char* emptyStr = "";        // Empty string

// 15. Testing Error Cases
@ # $ % ^ & * invalid_symbols
invalid-identifier-with-dash
123invalidIdentifier

// End of test cases