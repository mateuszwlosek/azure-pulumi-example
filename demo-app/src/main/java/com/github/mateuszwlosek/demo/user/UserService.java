package com.github.mateuszwlosek.demo.user;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class UserService {

	private final UserRepository repository;

	public List<User> findAllUsers() {
		log.info("Finding users ...");
		return repository.findAll();
	}

	public void createUser(final String username) {
		log.info("Creating user with username: {}", username);
		final User user = User.builder()
			.username(username)
			.build();

		repository.save(user);
	}
}
