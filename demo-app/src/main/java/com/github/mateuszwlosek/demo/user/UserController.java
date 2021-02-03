package com.github.mateuszwlosek.demo.user;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("user")
@RequiredArgsConstructor
public class UserController {

	private final UserService service;

	@GetMapping
	public List<User> getUsers() {
		return service.findAllUsers();
	}

	@PostMapping
	public void createUser(@RequestParam final String username) {
		service.createUser(username);
	}
}
