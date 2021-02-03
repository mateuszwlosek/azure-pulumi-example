package com.github.mateuszwlosek.demo.user;

import lombok.Builder;
import lombok.Data;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Builder
@ToString
@Document
public class User {

	@Id
	private String id;

	private String username;
}