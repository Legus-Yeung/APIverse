import { JwtService } from '@nestjs/jwt';
export interface User {
    username: string;
    password: string;
}
export interface UserData {
    [username: string]: string;
}
export declare class AuthService {
    private jwtService;
    private readonly usersFile;
    private users;
    constructor(jwtService: JwtService);
    private loadUsers;
    private saveUsers;
    register(user: User): Promise<{
        success: boolean;
        message: string;
    }>;
    login(user: User): Promise<{
        success: boolean;
        message: string;
        token: string;
    }>;
    validateUser(username: string): Promise<any>;
}
