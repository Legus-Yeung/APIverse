package com.example.banking.controller;

import com.example.banking.model.*;
import com.example.banking.service.AccountService;
import com.example.banking.service.JwtService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/accounts")
public class AccountControllerNoPrefix {
    
    @Autowired
    private AccountService accountService;
    
    @Autowired
    private JwtService jwtService;

    @PostMapping("/create")
    public ResponseEntity<ApiResponse> createAccount(
            @Valid @RequestBody AccountCreate accountCreate,
            @RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Account account = accountService.createAccount(username, accountCreate);
            
            Map<String, Object> data = new HashMap<>();
            data.put("account_number", account.getAccountNumber());
            data.put("balance", account.getBalance());
            
            return ResponseEntity.ok(new ApiResponse(true, "Account created successfully", data));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    @GetMapping("/my-account")
    public ResponseEntity<ApiResponse> getMyAccount(@RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Account account = accountService.getMyAccount(username);
            
            // Create a simplified account object for response
            Account responseAccount = new Account();
            responseAccount.setAccountNumber(account.getAccountNumber());
            responseAccount.setBalance(account.getBalance());
            responseAccount.setCreatedAt(account.getCreatedAt());
            
            return ResponseEntity.ok(new ApiResponse(true, null, responseAccount));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    @PostMapping("/deposit")
    public ResponseEntity<ApiResponse> deposit(
            @Valid @RequestBody AccountBalanceUpdate amountData,
            @RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Account account = accountService.deposit(username, amountData);
            
            Map<String, Object> data = new HashMap<>();
            data.put("new_balance", account.getBalance());
            
            return ResponseEntity.ok(new ApiResponse(true, 
                String.format("Deposited $%.2f", amountData.getAmount()), data));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    @PostMapping("/withdraw")
    public ResponseEntity<ApiResponse> withdraw(
            @Valid @RequestBody AccountBalanceUpdate amountData,
            @RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Account account = accountService.withdraw(username, amountData);
            
            Map<String, Object> data = new HashMap<>();
            data.put("new_balance", account.getBalance());
            
            return ResponseEntity.ok(new ApiResponse(true, 
                String.format("Withdrew $%.2f", amountData.getAmount()), data));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    @PostMapping("/transfer")
    public ResponseEntity<ApiResponse> transfer(
            @Valid @RequestBody AccountTransfer transferData,
            @RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            Account account = accountService.transfer(username, transferData);
            
            Map<String, Object> data = new HashMap<>();
            data.put("new_balance", account.getBalance());
            
            return ResponseEntity.ok(new ApiResponse(true, 
                String.format("Transferred $%.2f to account %s", 
                    transferData.getAmount(), transferData.getToAccountNumber()), data));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    @PostMapping("/close")
    public ResponseEntity<ApiResponse> closeAccount(@RequestHeader("Authorization") String authHeader) {
        try {
            String username = extractUsernameFromToken(authHeader);
            accountService.closeAccount(username);
            
            return ResponseEntity.ok(new ApiResponse(true, "Account closed successfully"));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                    .body(new ApiResponse(false, e.getMessage()));
        }
    }

    private String extractUsernameFromToken(String authHeader) {
        try {
            String token = authHeader.substring(7); // Remove "Bearer " prefix
            return jwtService.extractUsername(token);
        } catch (Exception e) {
            throw new RuntimeException("Invalid token");
        }
    }
}

