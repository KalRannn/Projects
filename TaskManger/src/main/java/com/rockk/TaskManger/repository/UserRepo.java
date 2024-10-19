package com.rockk.TaskManger.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Repository;

import com.rockk.TaskManger.entities.User;
import com.rockk.TaskManger.enums.UserRole;
@Repository
public interface UserRepo extends JpaRepository<User,Long>{

    Optional<User> findFirstByEmail(String username);

    Optional<User> findByUserRole(UserRole admin);

}
