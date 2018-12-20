-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.9-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for view catalogue.tracklengths
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `tracklengths` (
	`albumid` INT(11) NOT NULL,
	`disc` TINYINT(4) NOT NULL,
	`track` TINYINT(4) NOT NULL,
	`tracktitle` VARCHAR(255) NULL COLLATE 'utf8_unicode_ci',
	`tracklength` INT(8) NULL,
	`bonustrack` TINYINT(3) UNSIGNED ZEROFILL NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.tracklengths
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `tracklengths`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `tracklengths` AS select 		albumid, 
				disc, 
				track,
				tracktitle,
				hour(`track`.`Length`) * 3600 + minute(`track`.`Length`) * 60 + second(`track`.`Length`) AS `tracklength`,
				bonustrack
from			track
order by		albumid, disc, track ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
