-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.6.7-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table capstone_2023_tdsp2.exec_info
DROP TABLE IF EXISTS `exec_info`;
CREATE TABLE IF NOT EXISTS `exec_info` (
  `exec_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Execution instance identifier',
  `exec_start` datetime NOT NULL COMMENT 'Execution start time',
  `exec_stop` datetime DEFAULT NULL COMMENT 'Execution stop time',
  `input_size` int(11) NOT NULL COMMENT 'Quantity of people used as input',
  `output_size` int(11) NOT NULL COMMENT 'Quantity of people returned by model',
  `name` varchar(50) NOT NULL COMMENT 'Name of the run set by user.',
  PRIMARY KEY (`exec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='System execution logging and analytics core table.';

-- Data exporting was unselected.

-- Dumping structure for table capstone_2023_tdsp2.exec_input
DROP TABLE IF EXISTS `exec_input`;
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
DROP TABLE IF EXISTS `exec_model`;
CREATE TABLE IF NOT EXISTS `exec_model` (
  `model_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Model identifier',
  `exec_id` int(11) unsigned zerofill NOT NULL COMMENT 'Foreign key connecting model with correspinding execution instance',
  `tokenizer` varchar(50) NOT NULL COMMENT 'Pretrained tokenizer type used by transformer',
  `model` varchar(50) NOT NULL COMMENT 'Pretrained model type used by the embedder',
  `mod_start` datetime NOT NULL COMMENT 'Model start time',
  `mod_stop` datetime DEFAULT NULL COMMENT 'Model stop time',
  `device` varchar(50) NOT NULL COMMENT 'Compute method used by model; generally GPU or CPU.',
  `dim` int(11) NOT NULL COMMENT 'Dimension of the vectors in embedding.',
  PRIMARY KEY (`model_id`),
  KEY `Model_Exec_FK` (`exec_id`),
  CONSTRAINT `Model_Exec_FK` FOREIGN KEY (`exec_id`) REFERENCES `exec_info` (`exec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Model information related to specific instance of program execution.';

-- Data exporting was unselected.

-- Dumping structure for table capstone_2023_tdsp2.exec_output
DROP TABLE IF EXISTS `exec_output`;
CREATE TABLE IF NOT EXISTS `exec_output` (
  `output_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Output identifier',
  `exec_id` int(11) unsigned zerofill NOT NULL COMMENT 'Foreign key conneecting output to system execution instance',
  `person_id` int(11) unsigned NOT NULL COMMENT 'output person identifier',
  `k_value` float NOT NULL COMMENT 'Similarity value of output person to input',
  PRIMARY KEY (`output_id`),
  UNIQUE KEY `PERSON_EXEC_UNIQUE` (`exec_id`,`person_id`),
  CONSTRAINT `OUTPUT_EXEC_FK` FOREIGN KEY (`exec_id`) REFERENCES `exec_info` (`exec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Output data related to specific instances of program execution';

-- Data exporting was unselected.

-- Dumping structure for table capstone_2023_tdsp2.exec_pinecone
DROP TABLE IF EXISTS `exec_pinecone`;
CREATE TABLE IF NOT EXISTS `exec_pinecone` (
  `pinecone_id` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT COMMENT 'Core id for pinecone connection',
  `exec_id` int(11) unsigned zerofill NOT NULL COMMENT 'Foreign key to exec_info entry',
  `namespace` varchar(50) NOT NULL COMMENT 'Namepace used in pinecone upsert call',
  `index` varchar(50) NOT NULL COMMENT 'Index used to store embedding in pinecone',
  `upsert_start` datetime NOT NULL COMMENT 'Embedding upsert to pinecone index start time',
  `upsert_stop` datetime DEFAULT NULL COMMENT 'Embedding upsert to pinecone index stop time',
  `query_start` datetime NOT NULL COMMENT 'Query call to pinecone index start time',
  `query_stop` datetime DEFAULT NULL COMMENT 'Query call to pinecone index stop time',
  `kmin` float NOT NULL COMMENT 'Minimum similarity value in output people',
  `kmax` float NOT NULL COMMENT 'Maximum similarity value in output people',
  `kavg` float NOT NULL COMMENT 'Average similarity value across all output people',
  PRIMARY KEY (`pinecone_id`),
  KEY `Pinecone_Exec_FK` (`exec_id`),
  CONSTRAINT `Pinecone_Exec_FK` FOREIGN KEY (`exec_id`) REFERENCES `exec_info` (`exec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Statistics related to the pincone database connection used within the system.';

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
