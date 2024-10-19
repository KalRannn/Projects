package com.rockk.TaskManger.services.auth;

import com.rockk.TaskManger.dto.SignupRequest;
import com.rockk.TaskManger.dto.UserDto;

public interface AuthService {
    UserDto signupUser(SignupRequest signupRequest);
    boolean hasUserWithEmail(String email);
}
