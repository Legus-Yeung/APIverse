package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/mux"
	"golang.org/x/crypto/bcrypt"
)

const (
	SECRET_KEY     = "supersecretkey"
	USERS_FILE     = "users.json"
	ACCOUNTS_FILE  = "accounts.json"
	TOKEN_DURATION = 1 * time.Hour
)

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type AccountCreate struct {
	InitialBalance float64 `json:"initial_balance"`
}

type AccountBalanceUpdate struct {
	Amount float64 `json:"amount"`
}

type AccountTransfer struct {
	ToAccountNumber string  `json:"to_account_number"`
	Amount          float64 `json:"amount"`
}

type Account struct {
	AccountNumber string  `json:"account_number"`
	Username      string  `json:"username"`
	Balance       float64 `json:"balance"`
	IsActive      bool    `json:"is_active"`
	CreatedAt     string  `json:"created_at"`
}

type Response struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Token   string      `json:"token,omitempty"`
	Account *Account    `json:"account,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}

type ErrorResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
}

var users map[string]string
var accounts map[string]Account

func init() {
	users = make(map[string]string)
	loadUsers()
	accounts = make(map[string]Account)
	loadAccounts()
}

func loadUsers() {
	if _, err := os.Stat(USERS_FILE); os.IsNotExist(err) {
		saveUsers()
		return
	}

	data, err := os.ReadFile(USERS_FILE)
	if err != nil {
		log.Printf("Error reading users file: %v", err)
		return
	}

	if err := json.Unmarshal(data, &users); err != nil {
		log.Printf("Error unmarshaling users: %v", err)
		users = make(map[string]string)
	}
}

func saveUsers() {
	data, err := json.MarshalIndent(users, "", "    ")
	if err != nil {
		log.Printf("Error marshaling users: %v", err)
		return
	}

	if err := os.WriteFile(USERS_FILE, data, 0644); err != nil {
		log.Printf("Error writing users file: %v", err)
	}
}

func loadAccounts() {
	if _, err := os.Stat(ACCOUNTS_FILE); os.IsNotExist(err) {
		saveAccounts()
		return
	}

	data, err := os.ReadFile(ACCOUNTS_FILE)
	if err != nil {
		log.Printf("Error reading accounts file: %v", err)
		return
	}

	if err := json.Unmarshal(data, &accounts); err != nil {
		log.Printf("Error unmarshaling accounts: %v", err)
		accounts = make(map[string]Account)
	}
}

func saveAccounts() {
	data, err := json.MarshalIndent(accounts, "", "    ")
	if err != nil {
		log.Printf("Error marshaling accounts: %v", err)
		return
	}

	if err := os.WriteFile(ACCOUNTS_FILE, data, 0644); err != nil {
		log.Printf("Error writing accounts file: %v", err)
	}
}

func hashPassword(password string) (string, error) {
	hashedBytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(hashedBytes), err
}

func checkPassword(password, hashedPassword string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
	return err == nil
}

func generateToken(username string) (string, error) {
	claims := jwt.MapClaims{
		"username": username,
		"exp":      time.Now().Add(TOKEN_DURATION).Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(SECRET_KEY))
}

func verifyToken(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(SECRET_KEY), nil
	})

	if err != nil {
		return nil, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims, nil
	}

	return nil, fmt.Errorf("invalid token")
}

func generateAccountNumber() string {
	for {
		accountNumber := fmt.Sprintf("%010d", time.Now().UnixNano()%10000000000)
		if _, exists := accounts[accountNumber]; !exists {
			return accountNumber
		}
		time.Sleep(1 * time.Nanosecond)
	}
}

func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			http.Error(w, `{"success": false, "message": "Authorization header required"}`, http.StatusUnauthorized)
			return
		}

		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == authHeader {
			http.Error(w, `{"success": false, "message": "Bearer token required"}`, http.StatusUnauthorized)
			return
		}

		claims, err := verifyToken(tokenString)
		if err != nil {
			http.Error(w, `{"success": false, "message": "Invalid token"}`, http.StatusUnauthorized)
			return
		}

		r.Header.Set("X-Username", claims["username"].(string))
		next(w, r)
	}
}

func registerHandler(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, `{"success": false, "message": "Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	if _, exists := users[user.Username]; exists {
		http.Error(w, `{"success": false, "message": "User already exists"}`, http.StatusBadRequest)
		return
	}

	hashedPassword, err := hashPassword(user.Password)
	if err != nil {
		http.Error(w, `{"success": false, "message": "Error hashing password"}`, http.StatusInternalServerError)
		return
	}

	users[user.Username] = hashedPassword
	saveUsers()

	response := Response{
		Success: true,
		Message: "User registered successfully",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, `{"success": false, "message": "Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	hashedPassword, exists := users[user.Username]
	if !exists || !checkPassword(user.Password, hashedPassword) {
		http.Error(w, `{"success": false, "message": "Invalid credentials"}`, http.StatusUnauthorized)
		return
	}

	token, err := generateToken(user.Username)
	if err != nil {
		http.Error(w, `{"success": false, "message": "Error generating token"}`, http.StatusInternalServerError)
		return
	}

	response := Response{
		Success: true,
		Message: "Login successful",
		Token:   token,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func protectedHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")
	response := Response{
		Success: true,
		Message: fmt.Sprintf("Hello, %s!", username),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func createAccountHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")

	var accountData AccountCreate
	if err := json.NewDecoder(r.Body).Decode(&accountData); err != nil {
		http.Error(w, `{"success": false, "message": "Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	for _, account := range accounts {
		if account.Username == username && account.IsActive {
			http.Error(w, `{"success": false, "message": "User already has an active account"}`, http.StatusBadRequest)
			return
		}
	}

	accountNumber := generateAccountNumber()
	newAccount := Account{
		AccountNumber: accountNumber,
		Username:      username,
		Balance:       accountData.InitialBalance,
		IsActive:      true,
		CreatedAt:     time.Now().Format(time.RFC3339),
	}

	accounts[accountNumber] = newAccount
	saveAccounts()

	response := Response{
		Success: true,
		Message: "Account created successfully",
		Data: map[string]interface{}{
			"account_number": accountNumber,
			"balance":        accountData.InitialBalance,
		},
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func getMyAccountHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")

	for _, account := range accounts {
		if account.Username == username && account.IsActive {
			response := Response{
				Success: true,
				Account: &Account{
					AccountNumber: account.AccountNumber,
					Balance:       account.Balance,
					CreatedAt:     account.CreatedAt,
				},
			}

			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(response)
			return
		}
	}

	http.Error(w, `{"success": false, "message": "No active account found"}`, http.StatusNotFound)
}

func depositHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")

	var amountData AccountBalanceUpdate
	if err := json.NewDecoder(r.Body).Decode(&amountData); err != nil {
		http.Error(w, `{"success": false, "message": "Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	if amountData.Amount <= 0 {
		http.Error(w, `{"success": false, "message": "Amount must be positive"}`, http.StatusBadRequest)
		return
	}

	for accountNumber, account := range accounts {
		if account.Username == username && account.IsActive {
			account.Balance += amountData.Amount
			accounts[accountNumber] = account
			saveAccounts()

			response := Response{
				Success: true,
				Message: fmt.Sprintf("Deposited $%.2f", amountData.Amount),
				Data: map[string]interface{}{
					"new_balance": account.Balance,
				},
			}

			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(response)
			return
		}
	}

	http.Error(w, `{"success": false, "message": "No active account found"}`, http.StatusNotFound)
}

func withdrawHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")

	var amountData AccountBalanceUpdate
	if err := json.NewDecoder(r.Body).Decode(&amountData); err != nil {
		http.Error(w, `{"success": false, "message": "Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	if amountData.Amount <= 0 {
		http.Error(w, `{"success": false, "message": "Amount must be positive"}`, http.StatusBadRequest)
		return
	}

	for accountNumber, account := range accounts {
		if account.Username == username && account.IsActive {
			if account.Balance < amountData.Amount {
				http.Error(w, `{"success": false, "message": "Insufficient funds"}`, http.StatusBadRequest)
				return
			}

			account.Balance -= amountData.Amount
			accounts[accountNumber] = account
			saveAccounts()

			response := Response{
				Success: true,
				Message: fmt.Sprintf("Withdrew $%.2f", amountData.Amount),
				Data: map[string]interface{}{
					"new_balance": account.Balance,
				},
			}

			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(response)
			return
		}
	}

	http.Error(w, `{"success": false, "message": "No active account found"}`, http.StatusNotFound)
}

func transferHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")

	var transferData AccountTransfer
	if err := json.NewDecoder(r.Body).Decode(&transferData); err != nil {
		http.Error(w, `{"success": false, "message": "Invalid JSON"}`, http.StatusBadRequest)
		return
	}

	if transferData.Amount <= 0 {
		http.Error(w, `{"success": false, "message": "Amount must be positive"}`, http.StatusBadRequest)
		return
	}

	var senderAccount Account
	var senderAccountNumber string
	found := false

	for accountNumber, account := range accounts {
		if account.Username == username && account.IsActive {
			senderAccount = account
			senderAccountNumber = accountNumber
			found = true
			break
		}
	}

	if !found {
		http.Error(w, `{"success": false, "message": "No active account found"}`, http.StatusNotFound)
		return
	}

	recipientAccount, exists := accounts[transferData.ToAccountNumber]
	if !exists {
		http.Error(w, `{"success": false, "message": "Recipient account not found"}`, http.StatusNotFound)
		return
	}

	if !recipientAccount.IsActive {
		http.Error(w, `{"success": false, "message": "Recipient account is not active"}`, http.StatusBadRequest)
		return
	}

	if senderAccount.Balance < transferData.Amount {
		http.Error(w, `{"success": false, "message": "Insufficient funds"}`, http.StatusBadRequest)
		return
	}

	senderAccount.Balance -= transferData.Amount
	recipientAccount.Balance += transferData.Amount

	accounts[senderAccountNumber] = senderAccount
	accounts[transferData.ToAccountNumber] = recipientAccount
	saveAccounts()

	response := Response{
		Success: true,
		Message: fmt.Sprintf("Transferred $%.2f to account %s", transferData.Amount, transferData.ToAccountNumber),
		Data: map[string]interface{}{
			"new_balance": senderAccount.Balance,
		},
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func closeAccountHandler(w http.ResponseWriter, r *http.Request) {
	username := r.Header.Get("X-Username")

	for accountNumber, account := range accounts {
		if account.Username == username && account.IsActive {
			if account.Balance > 0 {
				http.Error(w, `{"success": false, "message": "Cannot close account with remaining balance. Please withdraw all funds first."}`, http.StatusBadRequest)
				return
			}

			account.IsActive = false
			accounts[accountNumber] = account
			saveAccounts()

			response := Response{
				Success: true,
				Message: "Account closed successfully",
			}

			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(response)
			return
		}
	}

	http.Error(w, `{"success": false, "message": "No active account found"}`, http.StatusNotFound)
}

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/register", registerHandler).Methods("POST")
	r.HandleFunc("/login", loginHandler).Methods("POST")

	r.HandleFunc("/protected", authMiddleware(protectedHandler)).Methods("GET")
	r.HandleFunc("/accounts/create", authMiddleware(createAccountHandler)).Methods("POST")
	r.HandleFunc("/accounts/my-account", authMiddleware(getMyAccountHandler)).Methods("GET")
	r.HandleFunc("/accounts/deposit", authMiddleware(depositHandler)).Methods("POST")
	r.HandleFunc("/accounts/withdraw", authMiddleware(withdrawHandler)).Methods("POST")
	r.HandleFunc("/accounts/transfer", authMiddleware(transferHandler)).Methods("POST")
	r.HandleFunc("/accounts/close", authMiddleware(closeAccountHandler)).Methods("POST")

	fmt.Println("Server starting on http://127.0.0.1:5000")
	log.Fatal(http.ListenAndServe(":5000", r))
}
