package com.example.banking.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public class AccountTransfer {
    @JsonProperty("to_account_number")
    @NotBlank(message = "Recipient account number is required")
    private String toAccountNumber;
    
    @NotNull(message = "Amount is required")
    @Positive(message = "Amount must be positive")
    private Double amount;

    public AccountTransfer() {}

    public AccountTransfer(String toAccountNumber, Double amount) {
        this.toAccountNumber = toAccountNumber;
        this.amount = amount;
    }

    public String getToAccountNumber() {
        return toAccountNumber;
    }

    public void setToAccountNumber(String toAccountNumber) {
        this.toAccountNumber = toAccountNumber;
    }

    public Double getAmount() {
        return amount;
    }

    public void setAmount(Double amount) {
        this.amount = amount;
    }
}
