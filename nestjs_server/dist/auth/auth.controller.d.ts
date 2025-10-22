import { AuthService } from './auth.service';
export declare class RegisterDto {
    username: string;
    password: string;
}
export declare class LoginDto {
    username: string;
    password: string;
}
export declare class AuthController {
    private authService;
    constructor(authService: AuthService);
    register(registerDto: RegisterDto): Promise<{
        success: boolean;
        message: string;
    }>;
    login(loginDto: LoginDto): Promise<{
        success: boolean;
        message: string;
        token: string;
    }>;
    protected(user: any): Promise<{
        success: boolean;
        message: string;
    }>;
}
