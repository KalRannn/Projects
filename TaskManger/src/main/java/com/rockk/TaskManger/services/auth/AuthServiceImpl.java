package com.rockk.TaskManger.services.auth;

import java.util.Optional;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.rockk.TaskManger.dto.SignupRequest;
import com.rockk.TaskManger.dto.UserDto;
import com.rockk.TaskManger.entities.User;
import com.rockk.TaskManger.enums.UserRole;
import com.rockk.TaskManger.repository.UserRepo;

import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService{

    private final UserRepo userRepo;

    @PostConstruct
    public void createAnAdminAccount(){
        Optional<User> optinalUser = userRepo.findByUserRole(UserRole.ADMIN);
        if(optinalUser.isEmpty()){
            User user = new User();
            user.setEmail("admin@test.com");
            user.setName("admin");
            user.setPassword(new BCryptPasswordEncoder().encode("admin"));
            user.setUserRole(UserRole.ADMIN);
            userRepo.save(user);
            System.out.println("Admin account created successfully!");
        }else{
            System.out.println("Admin account already exists");
        }
    }

    public UserDto signupUser(SignupRequest signupRequest) {
        User user =new User();
        user.setEmail(signupRequest.getEmail());
        user.setName(signupRequest.getName());
        user.setPassword(new BCryptPasswordEncoder().encode(signupRequest.getPassword()));
        user.setUserRole(UserRole.EMPLOYEE);
        User createdUser = userRepo.save(user);
        return createdUser.getUserDto();
    }

    @Override
    public boolean hasUserWithEmail(String email) {
        return userRepo.findFirstByEmail(email).isPresent();
    }
}
