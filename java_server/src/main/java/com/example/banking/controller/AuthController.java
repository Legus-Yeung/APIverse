package com.example.banking.controller;

import com.example.banking.model.ApiResponse;
import com.example.banking.model.User;
import com.example.banking.service.JwtService;
import com.example.banking.service.PasswordService;
import com.example.banking.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class AuthController {
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private PasswordService passwordService;
    
    @Autowired
    private JwtService jwtService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponse> register(@Valid @RequestBody User user) {
        try {
            // Hash the password before storing
            String hashedPassword = passwordService.hashPassword(user.getPassword());
            user.setPassword(hashedPassword);
            
            userService.registerUser(user);
            
            return ResponseEntity.ok(new ApiResponse(true, "User registered successfully"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse> login(@Valid @RequestBody User user) {
        try {
            // Load users and check credentials
            Map<String, String> users = userService.loadUsers();
            String storedPassword = users.get(user.getUsername());
            
            if (storedPassword == null || !passwordService.checkPassword(user.getPassword(), storedPassword)) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponse(false, "Invalid credentials"));
            }
            
            String token = jwtService.generateToken(user.getUsername());
            
            return ResponseEntity.ok(new ApiResponse(true, "Login successful", token));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(new ApiResponse(false, "Invalid credentials"));
        }
    }

    @GetMapping("/protected")
    public ResponseEntity<ApiResponse> protectedEndpoint(@RequestHeader("Authorization") String authHeader) {
        try {
            String token = authHeader.substring(7); // Remove "Bearer " prefix
            String username = jwtService.extractUsername(token);
            
            if (jwtService.validateToken(token, username)) {
                return ResponseEntity.ok(new ApiResponse(true, "Hello, " + username + "!"));
            } else {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ApiResponse(false, "Invalid token"));
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(new ApiResponse(false, "Invalid token"));
        }
    }

}
