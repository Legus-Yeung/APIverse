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
export declare class AccountCreateDto {
    initial_balance: number;
}
export declare class AccountBalanceUpdateDto {
    amount: number;
}
export declare class AccountTransferDto {
    to_account_number: string;
    amount: number;
}
export declare class AccountService {
    private readonly accountsFile;
    private accounts;
    constructor();
    private loadAccounts;
    private saveAccounts;
    private generateAccountNumber;
    createAccount(username: string, accountData: AccountCreateDto): Promise<any>;
    getMyAccount(username: string): Promise<any>;
    deposit(username: string, amountData: AccountBalanceUpdateDto): Promise<any>;
    withdraw(username: string, amountData: AccountBalanceUpdateDto): Promise<any>;
    transfer(username: string, transferData: AccountTransferDto): Promise<any>;
    closeAccount(username: string): Promise<any>;
}
