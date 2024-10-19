package com.rockk.TaskManger.dto;

import com.rockk.TaskManger.enums.UserRole;

import lombok.Data;

@Data
public class AuthResponse {
    private String jwt;
    private Long userId;
    private UserRole userRole;
}
