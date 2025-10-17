import { AccountService, AccountCreateDto, AccountBalanceUpdateDto, AccountTransferDto } from './account.service';
export declare class AccountController {
    private accountService;
    constructor(accountService: AccountService);
    createAccount(user: any, accountData: AccountCreateDto): Promise<any>;
    getMyAccount(user: any): Promise<any>;
    deposit(user: any, amountData: AccountBalanceUpdateDto): Promise<any>;
    withdraw(user: any, amountData: AccountBalanceUpdateDto): Promise<any>;
    transfer(user: any, transferData: AccountTransferDto): Promise<any>;
    closeAccount(user: any): Promise<any>;
}
