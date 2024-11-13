
CREATE TABLE IF NOT EXISTS `ecg`.`user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
);

CREATE TABLE IF NOT EXISTS `ecg`.`ecg` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `ecg`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `ecg`.`lead` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(3) NOT NULL,
  `samples` INT DEFAULT NULL,
  `signal` varchar(256) NOT NULL,
  `ecg_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `ecg_id_idx` (`ecg_id` ASC) VISIBLE,
  CONSTRAINT `ecg_id`
    FOREIGN KEY (`ecg_id`)
    REFERENCES `ecg`.`ecg` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

INSERT INTO `ecg`.`user` (`username`, `password`, `is_admin`)
  VALUES (
    'email@sample.com',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXNzd29yZCI6IjEyM19BbnN3ZXJfYWdhaW4ifQ.ky_fzkZUBwLaGK0gusrR3TkKF99dN39EpcCxdPbDeqs',
    1
);