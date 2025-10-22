import { Controller, Post, Get, Body, UseGuards } from '@nestjs/common';
import { AccountService, AccountCreateDto, AccountBalanceUpdateDto, AccountTransferDto } from './account.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { GetUser } from '../auth/get-user.decorator';

@Controller('accounts')
@UseGuards(JwtAuthGuard)
export class AccountController {
  constructor(private accountService: AccountService) {}

  @Post('create')
  async createAccount(@GetUser() user: any, @Body() accountData: AccountCreateDto) {
    return this.accountService.createAccount(user.username, accountData);
  }

  @Get('my-account')
  async getMyAccount(@GetUser() user: any) {
    return this.accountService.getMyAccount(user.username);
  }

  @Post('deposit')
  async deposit(@GetUser() user: any, @Body() amountData: AccountBalanceUpdateDto) {
    return this.accountService.deposit(user.username, amountData);
  }

  @Post('withdraw')
  async withdraw(@GetUser() user: any, @Body() amountData: AccountBalanceUpdateDto) {
    return this.accountService.withdraw(user.username, amountData);
  }

  @Post('transfer')
  async transfer(@GetUser() user: any, @Body() transferData: AccountTransferDto) {
    return this.accountService.transfer(user.username, transferData);
  }

  @Post('close')
  async closeAccount(@GetUser() user: any) {
    return this.accountService.closeAccount(user.username);
  }
}
