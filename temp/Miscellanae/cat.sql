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


-- Dumping database structure for catalogue
CREATE DATABASE IF NOT EXISTS `catalogue` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `catalogue`;

-- Dumping structure for table catalogue.album
CREATE TABLE IF NOT EXISTS `album` (
  `AlbumID` int(11) NOT NULL AUTO_INCREMENT,
  `Album` varchar(255) DEFAULT NULL,
  `YearReleased` smallint(5) unsigned DEFAULT NULL,
  `AlbumTypeID` int(11) DEFAULT NULL,
  `SourceID` int(11) DEFAULT NULL,
  `SourceAdditional` varchar(255) DEFAULT NULL,
  `CartridgeID` int(11) DEFAULT NULL,
  `LabelID` int(11) DEFAULT NULL,
  `DateAdded` datetime DEFAULT current_timestamp(),
  `DatePurchased` date DEFAULT NULL,
  `ArtistID` int(11) NOT NULL,
  PRIMARY KEY (`AlbumID`),
  KEY `FK_album_artist` (`ArtistID`),
  KEY `FK_album_source` (`SourceID`),
  KEY `FK_album_albumtype` (`AlbumTypeID`),
  CONSTRAINT `FK_album_albumtype` FOREIGN KEY (`AlbumTypeID`) REFERENCES `albumtype` (`AlbumTypeID`) ON DELETE SET NULL,
  CONSTRAINT `FK_album_artist` FOREIGN KEY (`ArtistID`) REFERENCES `artist` (`ArtistID`) ON DELETE CASCADE,
  CONSTRAINT `FK_album_source` FOREIGN KEY (`SourceID`) REFERENCES `source` (`SourceID`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=620 DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.album: ~0 rows (approximately)
DELETE FROM `album`;
/*!40000 ALTER TABLE `album` DISABLE KEYS */;
/*!40000 ALTER TABLE `album` ENABLE KEYS */;

-- Dumping structure for view catalogue.albumlengths
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `albumlengths` (
	`AlbumID` INT(11) NOT NULL,
	`AlbumLength` DECIMAL(32,0) NULL
) ENGINE=MyISAM;

-- Dumping structure for table catalogue.albumtype
CREATE TABLE IF NOT EXISTS `albumtype` (
  `AlbumTypeID` int(11) NOT NULL AUTO_INCREMENT,
  `AlbumType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`AlbumTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.albumtype: ~9 rows (approximately)
DELETE FROM `albumtype`;
/*!40000 ALTER TABLE `albumtype` DISABLE KEYS */;
INSERT INTO `albumtype` (`AlbumTypeID`, `AlbumType`) VALUES
	(1, 'Studio'),
	(2, 'Live'),
	(3, 'Single'),
	(4, 'EP'),
	(5, 'Compilation'),
	(6, 'Unofficial'),
	(7, 'Soundtrack'),
	(8, 'Spoken Word'),
	(9, 'Classical');
/*!40000 ALTER TABLE `albumtype` ENABLE KEYS */;

-- Dumping structure for table catalogue.artist
CREATE TABLE IF NOT EXISTS `artist` (
  `ArtistID` int(11) NOT NULL AUTO_INCREMENT,
  `ArtistName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ArtistID`)
) ENGINE=InnoDB AUTO_INCREMENT=265 DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.artist: ~0 rows (approximately)
DELETE FROM `artist`;
/*!40000 ALTER TABLE `artist` DISABLE KEYS */;
/*!40000 ALTER TABLE `artist` ENABLE KEYS */;

-- Dumping structure for view catalogue.chart_album_annual
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_album_annual` (
	`Y` INT(4) NULL,
	`ArtistName` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`Album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`LogTime` DECIMAL(54,0) NULL,
	`LogCount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_album_month
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_album_month` (
	`Y` INT(4) NULL,
	`M` INT(2) NULL,
	`ArtistName` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`Album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`LogTime` DECIMAL(54,0) NULL,
	`LogCount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_artist_annual
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_artist_annual` (
	`Y` INT(4) NULL,
	`ArtistName` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`LogTime` DECIMAL(54,0) NULL,
	`LogCount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_artist_month
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_artist_month` (
	`Y` INT(4) NULL,
	`M` INT(2) NULL,
	`ArtistName` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`LogTime` DECIMAL(54,0) NULL,
	`LogCount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for table catalogue.log
CREATE TABLE IF NOT EXISTS `log` (
  `LogID` int(11) NOT NULL AUTO_INCREMENT,
  `AlbumID` int(11) DEFAULT NULL,
  `LogDate` date DEFAULT NULL,
  PRIMARY KEY (`LogID`),
  KEY `FK__album` (`AlbumID`),
  CONSTRAINT `FK__album` FOREIGN KEY (`AlbumID`) REFERENCES `album` (`AlbumID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.log: ~0 rows (approximately)
DELETE FROM `log`;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
/*!40000 ALTER TABLE `log` ENABLE KEYS */;

-- Dumping structure for table catalogue.source
CREATE TABLE IF NOT EXISTS `source` (
  `SourceID` int(11) NOT NULL AUTO_INCREMENT,
  `Source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`SourceID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.source: ~4 rows (approximately)
DELETE FROM `source`;
/*!40000 ALTER TABLE `source` DISABLE KEYS */;
INSERT INTO `source` (`SourceID`, `Source`) VALUES
	(1, 'CD'),
	(2, 'Vinyl'),
	(3, 'Cassette'),
	(4, 'Digital');
/*!40000 ALTER TABLE `source` ENABLE KEYS */;

-- Dumping structure for table catalogue.track
CREATE TABLE IF NOT EXISTS `track` (
  `TrackID` int(11) NOT NULL AUTO_INCREMENT,
  `AlbumID` int(11) NOT NULL,
  `Disc` tinyint(4) NOT NULL,
  `Track` tinyint(4) NOT NULL,
  `TrackTitle` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `Length` time DEFAULT NULL,
  `BonusTrack` tinyint(3) unsigned zerofill NOT NULL DEFAULT 000,
  PRIMARY KEY (`TrackID`),
  KEY `FK_track_album` (`AlbumID`),
  CONSTRAINT `FK_track_album` FOREIGN KEY (`AlbumID`) REFERENCES `album` (`AlbumID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7249 DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.track: ~0 rows (approximately)
DELETE FROM `track`;
/*!40000 ALTER TABLE `track` DISABLE KEYS */;
/*!40000 ALTER TABLE `track` ENABLE KEYS */;

-- Dumping structure for view catalogue.albumlengths
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `albumlengths`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `albumlengths` AS SELECT album.AlbumID, SUM(track.Length) as AlbumLength
FROM album INNER JOIN track on album.AlbumID = track.AlbumID
WHERE track.BonusTrack = 0 
GROUP BY album.AlbumID ;

-- Dumping structure for view catalogue.chart_album_annual
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_album_annual`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `chart_album_annual` AS SELECT 		Year(log.LogDate) as Y, 
				artist.ArtistName, 
				album.Album, 
				SUM(albumlengths.AlbumLength) as LogTime, 
				COUNT(log.LogID) as LogCount

FROM 			albumlengths 
					INNER JOIN album on albumlengths.AlbumID = album.AlbumID
					INNER JOIN log on log.AlbumID = album.AlbumID
					INNER JOIN artist on album.ArtistID = artist.ArtistID
					
WHERE			album.AlbumTypeID NOT IN (3, 4, 8)
GROUP BY		Y, artist.ArtistName, Album.Album
ORDER BY		Y, LogTime DESC, LogCount DESC ;

-- Dumping structure for view catalogue.chart_album_month
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_album_month`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `chart_album_month` AS SELECT 		Year(log.LogDate) as Y, 
				Month(log.LogDate) as M,
				artist.ArtistName, 
				album.Album, 
				SUM(albumlengths.AlbumLength) as LogTime, 
				COUNT(log.LogID) as LogCount

FROM 			albumlengths 
					INNER JOIN album on albumlengths.AlbumID = album.AlbumID
					INNER JOIN log on log.AlbumID = album.AlbumID
					INNER JOIN artist on album.ArtistID = artist.ArtistID
					
WHERE			album.AlbumTypeID NOT IN (3, 4, 8)
GROUP BY		Y, M, artist.ArtistName, Album.Album
ORDER BY		Y, M, LogTime DESC, LogCount DESC ;

-- Dumping structure for view catalogue.chart_artist_annual
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_artist_annual`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `chart_artist_annual` AS SELECT 		Year(log.LogDate) as Y, 
				artist.ArtistName, 
				SUM(albumlengths.AlbumLength) as LogTime, 
				COUNT(log.LogID) as LogCount

FROM 			albumlengths 
					INNER JOIN album on albumlengths.AlbumID = album.AlbumID
					INNER JOIN log on log.AlbumID = album.AlbumID
					INNER JOIN artist on artist.ArtistID = album.ArtistID					
WHERE			album.AlbumTypeID NOT IN (3, 4, 8)
GROUP BY		Y, artist.ArtistName
ORDER BY		Y, LogTime DESC, LogCount DESC ;

-- Dumping structure for view catalogue.chart_artist_month
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_artist_month`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `chart_artist_month` AS SELECT 		Year(log.LogDate) as Y, 
				Month(log.LogDate) as M,
				artist.ArtistName, 
				SUM(albumlengths.AlbumLength) as LogTime, 
				COUNT(log.LogID) as LogCount

FROM 			albumlengths 
					INNER JOIN album on albumlengths.AlbumID = album.AlbumID
					INNER JOIN log on log.AlbumID = album.AlbumID
					INNER JOIN artist on artist.ArtistID = album.ArtistID					
WHERE			album.AlbumTypeID NOT IN (3, 4, 8)
GROUP BY		Y, M, artist.ArtistName
ORDER BY		Y, M, LogTime DESC, LogCount DESC ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
