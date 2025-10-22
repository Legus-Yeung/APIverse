package com.example.banking.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;

public class Account {
    @JsonProperty("account_number")
    private String accountNumber;
    
    private String username;
    private Double balance;
    
    @JsonProperty("is_active")
    private Boolean isActive = true;
    
    @JsonProperty("created_at")
    private String createdAt;

    public Account() {}

    public Account(String accountNumber, String username, Double balance, Boolean isActive, String createdAt) {
        this.accountNumber = accountNumber;
        this.username = username;
        this.balance = balance;
        this.isActive = isActive;
        this.createdAt = createdAt;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        this.accountNumber = accountNumber;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Double getBalance() {
        return balance;
    }

    public void setBalance(Double balance) {
        this.balance = balance;
    }

    public Boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(Boolean isActive) {
        this.isActive = isActive;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }
}
