-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.6.7-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table capstone_2023_tdsp2.exec_info
CREATE TABLE IF NOT EXISTS `exec_info` (
  `exec_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Execution instance identifier',
  `exec_start` datetime NOT NULL COMMENT 'Execution start time',
  `exec_stop` datetime DEFAULT NULL COMMENT 'Execution stop time',
  PRIMARY KEY (`exec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='System execution logging and analytics core table.';

-- Data exporting was unselected.

-- Dumping structure for table capstone_2023_tdsp2.exec_input
CREATE TABLE IF NOT EXISTS `exec_input` (
  `input_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Input identifier',
  `exec_id` int(11) unsigned zerofill NOT NULL COMMENT 'Foreign key connecting input to execution instance',
  `person_id` int(11) unsigned NOT NULL COMMENT 'Person identifier for input item',
  PRIMARY KEY (`input_id`),
  UNIQUE KEY `UNIQUE_EXEC_PERSON` (`exec_id`,`person_id`),
  CONSTRAINT `Input_Exec_FK` FOREIGN KEY (`exec_id`) REFERENCES `exec_info` (`exec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Input data related to program execution instances.';

-- Data exporting was unselected.

-- Dumping structure for table capstone_2023_tdsp2.exec_model
CREATE TABLE IF NOT EXISTS `exec_model` (
  `model_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Model identifier',
  `exec_id` int(11) unsigned zerofill NOT NULL COMMENT 'Foreign key connecting model with correspinding execution instance',
  `transformer_model` varchar(50) NOT NULL COMMENT 'Pretrained model type used by transformer',
  `mod_start` datetime NOT NULL COMMENT 'Model start time',
  `mod_stop` datetime DEFAULT NULL COMMENT 'Model stop time',
  PRIMARY KEY (`model_id`),
  KEY `Model_Exec_FK` (`exec_id`),
  CONSTRAINT `Model_Exec_FK` FOREIGN KEY (`exec_id`) REFERENCES `exec_info` (`exec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Model information related to specific instance of program execution.';

-- Data exporting was unselected.

-- Dumping structure for table capstone_2023_tdsp2.exec_output
CREATE TABLE IF NOT EXISTS `exec_output` (
  `output_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Output identifier',
  `exec_id` int(11) unsigned zerofill NOT NULL COMMENT 'Foreign key conneecting output to system execution instance',
  `person_id` int(11) unsigned NOT NULL COMMENT 'output person identifier',
  `k_value` decimal(3,2) NOT NULL COMMENT 'Similarity value of output person to input',
  PRIMARY KEY (`output_id`),
  UNIQUE KEY `PERSON_EXEC_UNIQUE` (`exec_id`,`person_id`),
  CONSTRAINT `OUTPUT_EXEC_FK` FOREIGN KEY (`exec_id`) REFERENCES `exec_info` (`exec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Output data related to specific instances of program execution';

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
