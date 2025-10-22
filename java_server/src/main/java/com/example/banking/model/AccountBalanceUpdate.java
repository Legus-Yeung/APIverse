package com.example.banking.model;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public class AccountBalanceUpdate {
    @NotNull(message = "Amount is required")
    @Positive(message = "Amount must be positive")
    private Double amount;

    public AccountBalanceUpdate() {}

    public AccountBalanceUpdate(Double amount) {
        this.amount = amount;
    }

    public Double getAmount() {
        return amount;
    }

    public void setAmount(Double amount) {
        this.amount = amount;
    }
}
