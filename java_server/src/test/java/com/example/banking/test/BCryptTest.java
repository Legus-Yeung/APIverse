package com.example.banking.test;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class BCryptTest {
    public static void main(String[] args) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        
        String password = "debugpass";
        String hash = "$2a$10$9lQYhtx16X4vRrhVZoulZuI2i9xZxuB1g53acbQoZCtjeTJWXYV76";
        
        System.out.println("Password: " + password);
        System.out.println("Hash: " + hash);
        System.out.println("Match: " + encoder.matches(password, hash));
        
        // Test with a fresh hash
        String newHash = encoder.encode(password);
        System.out.println("New hash: " + newHash);
        System.out.println("New match: " + encoder.matches(password, newHash));
    }
}
