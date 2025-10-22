package com.example.banking.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;

public class AccountCreate {
    @JsonProperty("initial_balance")
    @NotNull(message = "Initial balance is required")
    @PositiveOrZero(message = "Initial balance must be positive or zero")
    private Double initialBalance = 0.0;

    public AccountCreate() {}

    public AccountCreate(Double initialBalance) {
        this.initialBalance = initialBalance;
    }

    public Double getInitialBalance() {
        return initialBalance;
    }

    public void setInitialBalance(Double initialBalance) {
        this.initialBalance = initialBalance;
    }
}
