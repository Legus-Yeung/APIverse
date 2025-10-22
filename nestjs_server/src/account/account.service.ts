import { Injectable, NotFoundException, BadRequestException, ConflictException } from '@nestjs/common';
import { IsNumber, IsString, IsNotEmpty, IsOptional } from 'class-validator';
import * as fs from 'fs';
import * as path from 'path';

export interface Account {
  account_number: string;
  username: string;
  balance: number;
  is_active: boolean;
  created_at: string;
}

export interface AccountData {
  [accountNumber: string]: Account;
}

export class AccountCreateDto {
  @IsNumber()
  @IsOptional()
  initial_balance: number = 0.0;
}

export class AccountBalanceUpdateDto {
  @IsNumber()
  @IsNotEmpty()
  amount: number;
}

export class AccountTransferDto {
  @IsString()
  @IsNotEmpty()
  to_account_number: string;

  @IsNumber()
  @IsNotEmpty()
  amount: number;
}

@Injectable()
export class AccountService {
  private readonly accountsFile = 'accounts.json';
  private accounts: AccountData = {};

  constructor() {
    this.loadAccounts();
  }

  private loadAccounts(): void {
    const filePath = path.join(process.cwd(), this.accountsFile);
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      this.accounts = JSON.parse(data);
    } else {
      this.saveAccounts();
    }
  }

  private saveAccounts(): void {
    const filePath = path.join(process.cwd(), this.accountsFile);
    fs.writeFileSync(filePath, JSON.stringify(this.accounts, null, 4));
  }

  private generateAccountNumber(): string {
    let accountNumber: string;
    do {
      accountNumber = Math.floor(Math.random() * 10000000000).toString().padStart(10, '0');
    } while (this.accounts[accountNumber]);
    return accountNumber;
  }

  async createAccount(username: string, accountData: AccountCreateDto): Promise<any> {
    // Check if user already has an active account
    for (const account of Object.values(this.accounts)) {
      if (account.username === username && account.is_active) {
        throw new ConflictException('User already has an active account');
      }
    }

    const accountNumber = this.generateAccountNumber();
    const newAccount: Account = {
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

  async getMyAccount(username: string): Promise<any> {
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

    throw new NotFoundException('No active account found');
  }

  async deposit(username: string, amountData: AccountBalanceUpdateDto): Promise<any> {
    if (amountData.amount <= 0) {
      throw new BadRequestException('Amount must be positive');
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

    throw new NotFoundException('No active account found');
  }

  async withdraw(username: string, amountData: AccountBalanceUpdateDto): Promise<any> {
    if (amountData.amount <= 0) {
      throw new BadRequestException('Amount must be positive');
    }

    for (const accountNumber in this.accounts) {
      const account = this.accounts[accountNumber];
      if (account.username === username && account.is_active) {
        if (account.balance < amountData.amount) {
          throw new BadRequestException('Insufficient funds');
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

    throw new NotFoundException('No active account found');
  }

  async transfer(username: string, transferData: AccountTransferDto): Promise<any> {
    if (transferData.amount <= 0) {
      throw new BadRequestException('Amount must be positive');
    }

    // Find sender account
    let senderAccount: Account | null = null;
    let senderAccountNumber: string | null = null;

    for (const accountNumber in this.accounts) {
      const account = this.accounts[accountNumber];
      if (account.username === username && account.is_active) {
        senderAccount = account;
        senderAccountNumber = accountNumber;
        break;
      }
    }

    if (!senderAccount) {
      throw new NotFoundException('No active account found');
    }

    // Check recipient account
    const recipientAccount = this.accounts[transferData.to_account_number];
    if (!recipientAccount) {
      throw new NotFoundException('Recipient account not found');
    }

    if (!recipientAccount.is_active) {
      throw new BadRequestException('Recipient account is not active');
    }

    if (senderAccount.balance < transferData.amount) {
      throw new BadRequestException('Insufficient funds');
    }

    // Perform transfer
    senderAccount.balance -= transferData.amount;
    recipientAccount.balance += transferData.amount;
    this.saveAccounts();

    return {
      success: true,
      message: `Transferred $${transferData.amount.toFixed(2)} to account ${transferData.to_account_number}`,
      new_balance: senderAccount.balance,
    };
  }

  async closeAccount(username: string): Promise<any> {
    for (const accountNumber in this.accounts) {
      const account = this.accounts[accountNumber];
      if (account.username === username && account.is_active) {
        if (account.balance > 0) {
          throw new BadRequestException('Cannot close account with remaining balance. Please withdraw all funds first.');
        }

        account.is_active = false;
        this.saveAccounts();

        return {
          success: true,
          message: 'Account closed successfully',
        };
      }
    }

    throw new NotFoundException('No active account found');
  }
}