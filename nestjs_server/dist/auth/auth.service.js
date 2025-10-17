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
exports.AuthService = void 0;
const common_1 = require("@nestjs/common");
const jwt_1 = require("@nestjs/jwt");
const bcrypt = require("bcrypt");
const fs = require("fs");
const path = require("path");
let AuthService = class AuthService {
    constructor(jwtService) {
        this.jwtService = jwtService;
        this.usersFile = 'users.json';
        this.users = {};
        this.loadUsers();
    }
    loadUsers() {
        const filePath = path.join(process.cwd(), this.usersFile);
        if (fs.existsSync(filePath)) {
            const data = fs.readFileSync(filePath, 'utf8');
            this.users = JSON.parse(data);
        }
        else {
            this.saveUsers();
        }
    }
    saveUsers() {
        const filePath = path.join(process.cwd(), this.usersFile);
        fs.writeFileSync(filePath, JSON.stringify(this.users, null, 4));
    }
    async register(user) {
        if (this.users[user.username]) {
            throw new common_1.ConflictException('User already exists');
        }
        const hashedPassword = await bcrypt.hash(user.password, 10);
        this.users[user.username] = hashedPassword;
        this.saveUsers();
        return {
            success: true,
            message: 'User registered successfully',
        };
    }
    async login(user) {
        const hashedPassword = this.users[user.username];
        if (!hashedPassword || !(await bcrypt.compare(user.password, hashedPassword))) {
            throw new common_1.UnauthorizedException('Invalid credentials');
        }
        const payload = { username: user.username };
        const token = this.jwtService.sign(payload);
        return {
            success: true,
            message: 'Login successful',
            token,
        };
    }
    async validateUser(username) {
        if (this.users[username]) {
            return { username };
        }
        return null;
    }
};
exports.AuthService = AuthService;
exports.AuthService = AuthService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [jwt_1.JwtService])
], AuthService);
//# sourceMappingURL=auth.service.js.map