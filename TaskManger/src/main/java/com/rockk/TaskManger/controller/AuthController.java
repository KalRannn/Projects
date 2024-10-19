package com.rockk.TaskManger.controller;

import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.rockk.TaskManger.dto.AuthRequest;
import com.rockk.TaskManger.dto.AuthResponse;
import com.rockk.TaskManger.dto.SignupRequest;
import com.rockk.TaskManger.dto.UserDto;
import com.rockk.TaskManger.entities.User;
import com.rockk.TaskManger.repository.UserRepo;
import com.rockk.TaskManger.services.UserService;
import com.rockk.TaskManger.services.auth.AuthService;
import com.rockk.TaskManger.utils.JwtUtil;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    private final UserRepo userRepo;

    private final JwtUtil jwtUtil;

    private final UserService userService;

    private final AuthenticationManager authenticationManager;


    @PostMapping("/signup")
    public ResponseEntity<?> signupUser(@RequestBody SignupRequest signupRequest){
        if(authService.hasUserWithEmail(signupRequest.getEmail())){
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body("User already exists with this email");
        }
        UserDto createdUserDto = authService.signupUser(signupRequest);
        if(createdUserDto==null){return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("User not created");}
        return ResponseEntity.status(HttpStatus.CREATED).body(createdUserDto);
    }

    @PostMapping("/login")
    public AuthResponse login(@RequestBody AuthRequest authRequest){
        try{
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(authRequest.getEmail(), authRequest.getPassword()));
        }
        catch(BadCredentialsException e){
            throw new BadCredentialsException("Incorrect username or password");
        }
        final UserDetails userDetails = userService.userDetailsService().loadUserByUsername(authRequest.getEmail());
        Optional<User> optionalUser =userRepo.findFirstByEmail(authRequest.getEmail());
        final String jwtToken = jwtUtil.generateToken(userDetails);
        AuthResponse authResponse = new AuthResponse();
        if(optionalUser.isPresent()){
            authResponse.setJwt(jwtToken);
            authResponse.setUserId(optionalUser.get().getId());
            authResponse.setUserRole(optionalUser.get().getUserRole());
        }
        return authResponse;
    }
}
