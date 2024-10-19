package com.rockk.TaskManger.dto;

import com.rockk.TaskManger.enums.UserRole;

import lombok.Data;

@Data
public class UserDto {

    private Long id;
    private String name;
    private String email;
    private String password;
    private UserRole userRole;
}

