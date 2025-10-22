package com.example.banking.service;

import com.example.banking.model.Account;
import com.example.banking.model.AccountCreate;
import com.example.banking.model.AccountBalanceUpdate;
import com.example.banking.model.AccountTransfer;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class AccountService {
    
    @Value("${app.accounts.file:accounts.json}")
    private String accountsFile;
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    public Map<String, Account> loadAccounts() {
        try {
            File file = new File(accountsFile);
            if (!file.exists()) {
                saveAccounts(new HashMap<>());
                return new HashMap<>();
            }
            return objectMapper.readValue(file, new TypeReference<Map<String, Account>>() {});
        } catch (IOException e) {
            throw new RuntimeException("Failed to load accounts", e);
        }
    }

    public void saveAccounts(Map<String, Account> accounts) {
        try {
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(new File(accountsFile), accounts);
        } catch (IOException e) {
            throw new RuntimeException("Failed to save accounts", e);
        }
    }

    public String generateAccountNumber() {
        while (true) {
            String accountNumber = UUID.randomUUID().toString().replace("-", "").substring(0, 10);
            Map<String, Account> accounts = loadAccounts();
            if (!accounts.containsKey(accountNumber)) {
                return accountNumber;
            }
        }
    }

    public Account createAccount(String username, AccountCreate accountCreate) {
        Map<String, Account> accounts = loadAccounts();
        
        // Check if user already has an active account
        for (Account account : accounts.values()) {
            if (account.getUsername().equals(username) && account.getIsActive()) {
                throw new RuntimeException("User already has an active account");
            }
        }
        
        String accountNumber = generateAccountNumber();
        Account newAccount = new Account(
            accountNumber,
            username,
            accountCreate.getInitialBalance(),
            true,
            LocalDateTime.now().format(formatter)
        );
        
        accounts.put(accountNumber, newAccount);
        saveAccounts(accounts);
        
        return newAccount;
    }

    public Account getMyAccount(String username) {
        Map<String, Account> accounts = loadAccounts();
        
        for (Account account : accounts.values()) {
            if (account.getUsername().equals(username) && account.getIsActive()) {
                return account;
            }
        }
        
        throw new RuntimeException("No active account found");
    }

    public Account deposit(String username, AccountBalanceUpdate amountData) {
        Map<String, Account> accounts = loadAccounts();
        
        for (Map.Entry<String, Account> entry : accounts.entrySet()) {
            Account account = entry.getValue();
            if (account.getUsername().equals(username) && account.getIsActive()) {
                account.setBalance(account.getBalance() + amountData.getAmount());
                saveAccounts(accounts);
                return account;
            }
        }
        
        throw new RuntimeException("No active account found");
    }

    public Account withdraw(String username, AccountBalanceUpdate amountData) {
        Map<String, Account> accounts = loadAccounts();
        
        for (Map.Entry<String, Account> entry : accounts.entrySet()) {
            Account account = entry.getValue();
            if (account.getUsername().equals(username) && account.getIsActive()) {
                if (account.getBalance() < amountData.getAmount()) {
                    throw new RuntimeException("Insufficient funds");
                }
                
                account.setBalance(account.getBalance() - amountData.getAmount());
                saveAccounts(accounts);
                return account;
            }
        }
        
        throw new RuntimeException("No active account found");
    }

    public Account transfer(String username, AccountTransfer transferData) {
        Map<String, Account> accounts = loadAccounts();
        
        // Find sender account
        Account senderAccount = null;
        String senderAccountNumber = null;
        for (Map.Entry<String, Account> entry : accounts.entrySet()) {
            Account account = entry.getValue();
            if (account.getUsername().equals(username) && account.getIsActive()) {
                senderAccount = account;
                senderAccountNumber = entry.getKey();
                break;
            }
        }
        
        if (senderAccount == null) {
            throw new RuntimeException("No active account found");
        }
        
        // Check recipient account
        Account recipientAccount = accounts.get(transferData.getToAccountNumber());
        if (recipientAccount == null) {
            throw new RuntimeException("Recipient account not found");
        }
        
        if (!recipientAccount.getIsActive()) {
            throw new RuntimeException("Recipient account is not active");
        }
        
        if (senderAccount.getBalance() < transferData.getAmount()) {
            throw new RuntimeException("Insufficient funds");
        }
        
        // Perform transfer
        senderAccount.setBalance(senderAccount.getBalance() - transferData.getAmount());
        recipientAccount.setBalance(recipientAccount.getBalance() + transferData.getAmount());
        
        saveAccounts(accounts);
        return senderAccount;
    }

    public void closeAccount(String username) {
        Map<String, Account> accounts = loadAccounts();
        
        for (Map.Entry<String, Account> entry : accounts.entrySet()) {
            Account account = entry.getValue();
            if (account.getUsername().equals(username) && account.getIsActive()) {
                if (account.getBalance() > 0) {
                    throw new RuntimeException("Cannot close account with remaining balance. Please withdraw all funds first.");
                }
                
                account.setIsActive(false);
                saveAccounts(accounts);
                return;
            }
        }
        
        throw new RuntimeException("No active account found");
    }
}
