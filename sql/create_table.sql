DROP TABLE IF EXISTS `tasks`;
SET character_set_client = utf8mb4 ;

CREATE TABLE `tasks` (
  `task_id` int unsigned NOT NULL AUTO_INCREMENT,
  `task_title` varchar(45) NOT NULL,
  `task_status` enum('active','closed') NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`task_id`),
  UNIQUE KEY `task_id_UNIQUE` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `pre_tasks`;
SET character_set_client = utf8mb4 ;

CREATE TABLE `pre_tasks` (
  `task_id` int NOT NULL,
  `pre_task_id` int NOT NULL,
  PRIMARY KEY (`task_id`,`pre_task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;