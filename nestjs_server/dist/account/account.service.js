"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AccountService = exports.AccountTransferDto = exports.AccountBalanceUpdateDto = exports.AccountCreateDto = void 0;
const common_1 = require("@nestjs/common");
const class_validator_1 = require("class-validator");
const fs = require("fs");
const path = require("path");
class AccountCreateDto {
    constructor() {
        this.initial_balance = 0.0;
    }
}
exports.AccountCreateDto = AccountCreateDto;
__decorate([
    (0, class_validator_1.IsNumber)(),
    (0, class_validator_1.IsOptional)(),
    __metadata("design:type", Number)
], AccountCreateDto.prototype, "initial_balance", void 0);
class AccountBalanceUpdateDto {
}
exports.AccountBalanceUpdateDto = AccountBalanceUpdateDto;
__decorate([
    (0, class_validator_1.IsNumber)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", Number)
], AccountBalanceUpdateDto.prototype, "amount", void 0);
class AccountTransferDto {
}
exports.AccountTransferDto = AccountTransferDto;
__decorate([
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", String)
], AccountTransferDto.prototype, "to_account_number", void 0);
__decorate([
    (0, class_validator_1.IsNumber)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", Number)
], AccountTransferDto.prototype, "amount", void 0);
let AccountService = class AccountService {
    constructor() {
        this.accountsFile = 'accounts.json';
        this.accounts = {};
        this.loadAccounts();
    }
    loadAccounts() {
        const filePath = path.join(process.cwd(), this.accountsFile);
        if (fs.existsSync(filePath)) {
            const data = fs.readFileSync(filePath, 'utf8');
            this.accounts = JSON.parse(data);
        }
        else {
            this.saveAccounts();
        }
    }
    saveAccounts() {
        const filePath = path.join(process.cwd(), this.accountsFile);
        fs.writeFileSync(filePath, JSON.stringify(this.accounts, null, 4));
    }
    generateAccountNumber() {
        let accountNumber;
        do {
            accountNumber = Math.floor(Math.random() * 10000000000).toString().padStart(10, '0');
        } while (this.accounts[accountNumber]);
        return accountNumber;
    }
    async createAccount(username, accountData) {
        for (const account of Object.values(this.accounts)) {
            if (account.username === username && account.is_active) {
                throw new common_1.ConflictException('User already has an active account');
            }
        }
        const accountNumber = this.generateAccountNumber();
        const newAccount = {
            account_number: accountNumber,
            username,
            balance: accountData.initial_balance,
            is_active: true,
            created_at: new Date().toISOString(),
        };
        this.accounts[accountNumber] = newAccount;
        this.saveAccounts();
        return {
            success: true,
            message: 'Account created successfully',
            account_number: accountNumber,
            balance: accountData.initial_balance,
        };
    }
    async getMyAccount(username) {
        for (const account of Object.values(this.accounts)) {
            if (account.username === username && account.is_active) {
                return {
                    success: true,
                    account: {
                        account_number: account.account_number,
                        balance: account.balance,
                        created_at: account.created_at,
                    },
                };
            }
        }
        throw new common_1.NotFoundException('No active account found');
    }
    async deposit(username, amountData) {
        if (amountData.amount <= 0) {
            throw new common_1.BadRequestException('Amount must be positive');
        }
        for (const accountNumber in this.accounts) {
            const account = this.accounts[accountNumber];
            if (account.username === username && account.is_active) {
                account.balance += amountData.amount;
                this.saveAccounts();
                return {
                    success: true,
                    message: `Deposited $${amountData.amount.toFixed(2)}`,
                    new_balance: account.balance,
                };
            }
        }
        throw new common_1.NotFoundException('No active account found');
    }
    async withdraw(username, amountData) {
        if (amountData.amount <= 0) {
            throw new common_1.BadRequestException('Amount must be positive');
        }
        for (const accountNumber in this.accounts) {
            const account = this.accounts[accountNumber];
            if (account.username === username && account.is_active) {
                if (account.balance < amountData.amount) {
                    throw new common_1.BadRequestException('Insufficient funds');
                }
                account.balance -= amountData.amount;
                this.saveAccounts();
                return {
                    success: true,
                    message: `Withdrew $${amountData.amount.toFixed(2)}`,
                    new_balance: account.balance,
                };
            }
        }
        throw new common_1.NotFoundException('No active account found');
    }
    async transfer(username, transferData) {
        if (transferData.amount <= 0) {
            throw new common_1.BadRequestException('Amount must be positive');
        }
        let senderAccount = null;
        let senderAccountNumber = null;
        for (const accountNumber in this.accounts) {
            const account = this.accounts[accountNumber];
            if (account.username === username && account.is_active) {
                senderAccount = account;
                senderAccountNumber = accountNumber;
                break;
            }
        }
        if (!senderAccount) {
            throw new common_1.NotFoundException('No active account found');
        }
        const recipientAccount = this.accounts[transferData.to_account_number];
        if (!recipientAccount) {
            throw new common_1.NotFoundException('Recipient account not found');
        }
        if (!recipientAccount.is_active) {
            throw new common_1.BadRequestException('Recipient account is not active');
        }
        if (senderAccount.balance < transferData.amount) {
            throw new common_1.BadRequestException('Insufficient funds');
        }
        senderAccount.balance -= transferData.amount;
        recipientAccount.balance += transferData.amount;
        this.saveAccounts();
        return {
            success: true,
            message: `Transferred $${transferData.amount.toFixed(2)} to account ${transferData.to_account_number}`,
            new_balance: senderAccount.balance,
        };
    }
    async closeAccount(username) {
        for (const accountNumber in this.accounts) {
            const account = this.accounts[accountNumber];
            if (account.username === username && account.is_active) {
                if (account.balance > 0) {
                    throw new common_1.BadRequestException('Cannot close account with remaining balance. Please withdraw all funds first.');
                }
                account.is_active = false;
                this.saveAccounts();
                return {
                    success: true,
                    message: 'Account closed successfully',
                };
            }
        }
        throw new common_1.NotFoundException('No active account found');
    }
};
exports.AccountService = AccountService;
exports.AccountService = AccountService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [])
], AccountService);
//# sourceMappingURL=account.service.js.map