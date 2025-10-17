import { Injectable, UnauthorizedException, ConflictException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';
import * as fs from 'fs';
import * as path from 'path';

export interface User {
  username: string;
  password: string;
}

export interface UserData {
  [username: string]: string;
}

@Injectable()
export class AuthService {
  private readonly usersFile = 'users.json';
  private users: UserData = {};

  constructor(private jwtService: JwtService) {
    this.loadUsers();
  }

  private loadUsers(): void {
    const filePath = path.join(process.cwd(), this.usersFile);
    if (fs.existsSync(filePath)) {
      const data = fs.readFileSync(filePath, 'utf8');
      this.users = JSON.parse(data);
    } else {
      this.saveUsers();
    }
  }

  private saveUsers(): void {
    const filePath = path.join(process.cwd(), this.usersFile);
    fs.writeFileSync(filePath, JSON.stringify(this.users, null, 4));
  }

  async register(user: User): Promise<{ success: boolean; message: string }> {
    if (this.users[user.username]) {
      throw new ConflictException('User already exists');
    }

    const hashedPassword = await bcrypt.hash(user.password, 10);
    this.users[user.username] = hashedPassword;
    this.saveUsers();

    return {
      success: true,
      message: 'User registered successfully',
    };
  }

  async login(user: User): Promise<{ success: boolean; message: string; token: string }> {
    const hashedPassword = this.users[user.username];
    if (!hashedPassword || !(await bcrypt.compare(user.password, hashedPassword))) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const payload = { username: user.username };
    const token = this.jwtService.sign(payload);

    return {
      success: true,
      message: 'Login successful',
      token,
    };
  }

  async validateUser(username: string): Promise<any> {
    if (this.users[username]) {
      return { username };
    }
    return null;
  }
}
