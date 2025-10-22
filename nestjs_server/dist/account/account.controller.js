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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AccountController = void 0;
const common_1 = require("@nestjs/common");
const account_service_1 = require("./account.service");
const jwt_auth_guard_1 = require("../auth/jwt-auth.guard");
const get_user_decorator_1 = require("../auth/get-user.decorator");
let AccountController = class AccountController {
    constructor(accountService) {
        this.accountService = accountService;
    }
    async createAccount(user, accountData) {
        return this.accountService.createAccount(user.username, accountData);
    }
    async getMyAccount(user) {
        return this.accountService.getMyAccount(user.username);
    }
    async deposit(user, amountData) {
        return this.accountService.deposit(user.username, amountData);
    }
    async withdraw(user, amountData) {
        return this.accountService.withdraw(user.username, amountData);
    }
    async transfer(user, transferData) {
        return this.accountService.transfer(user.username, transferData);
    }
    async closeAccount(user) {
        return this.accountService.closeAccount(user.username);
    }
};
exports.AccountController = AccountController;
__decorate([
    (0, common_1.Post)('create'),
    __param(0, (0, get_user_decorator_1.GetUser)()),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, account_service_1.AccountCreateDto]),
    __metadata("design:returntype", Promise)
], AccountController.prototype, "createAccount", null);
__decorate([
    (0, common_1.Get)('my-account'),
    __param(0, (0, get_user_decorator_1.GetUser)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object]),
    __metadata("design:returntype", Promise)
], AccountController.prototype, "getMyAccount", null);
__decorate([
    (0, common_1.Post)('deposit'),
    __param(0, (0, get_user_decorator_1.GetUser)()),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, account_service_1.AccountBalanceUpdateDto]),
    __metadata("design:returntype", Promise)
], AccountController.prototype, "deposit", null);
__decorate([
    (0, common_1.Post)('withdraw'),
    __param(0, (0, get_user_decorator_1.GetUser)()),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, account_service_1.AccountBalanceUpdateDto]),
    __metadata("design:returntype", Promise)
], AccountController.prototype, "withdraw", null);
__decorate([
    (0, common_1.Post)('transfer'),
    __param(0, (0, get_user_decorator_1.GetUser)()),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, account_service_1.AccountTransferDto]),
    __metadata("design:returntype", Promise)
], AccountController.prototype, "transfer", null);
__decorate([
    (0, common_1.Post)('close'),
    __param(0, (0, get_user_decorator_1.GetUser)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object]),
    __metadata("design:returntype", Promise)
], AccountController.prototype, "closeAccount", null);
exports.AccountController = AccountController = __decorate([
    (0, common_1.Controller)('accounts'),
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    __metadata("design:paramtypes", [account_service_1.AccountService])
], AccountController);
//# sourceMappingURL=account.controller.js.map