package com.example.banking.service;

import com.example.banking.model.User;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class UserService {
    
    @Value("${app.users.file:users.json}")
    private String usersFile;
    
    private final ObjectMapper objectMapper = new ObjectMapper();

    public Map<String, String> loadUsers() {
        try {
            File file = new File(usersFile);
            if (!file.exists()) {
                saveUsers(new HashMap<>());
                return new HashMap<>();
            }
            return objectMapper.readValue(file, new TypeReference<Map<String, String>>() {});
        } catch (IOException e) {
            throw new RuntimeException("Failed to load users", e);
        }
    }

    public void saveUsers(Map<String, String> users) {
        try {
            objectMapper.writerWithDefaultPrettyPrinter().writeValue(new File(usersFile), users);
        } catch (IOException e) {
            throw new RuntimeException("Failed to save users", e);
        }
    }

    public void registerUser(User user) {
        Map<String, String> users = loadUsers();
        
        if (users.containsKey(user.getUsername())) {
            throw new RuntimeException("User already exists");
        }
        
        users.put(user.getUsername(), user.getPassword());
        saveUsers(users);
    }

    public boolean authenticateUser(User user) {
        Map<String, String> users = loadUsers();
        String storedPassword = users.get(user.getUsername());
        
        if (storedPassword == null) {
            return false;
        }
        
        return storedPassword.equals(user.getPassword());
    }
}
