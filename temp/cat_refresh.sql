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
DROP DATABASE IF EXISTS `catalogue`;
CREATE DATABASE IF NOT EXISTS `catalogue` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `catalogue`;

-- Dumping structure for table catalogue.album
DROP TABLE IF EXISTS `album`;
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
  KEY `FK_album_label` (`LabelID`),
  CONSTRAINT `FK_album_albumtype` FOREIGN KEY (`AlbumTypeID`) REFERENCES `albumtype` (`AlbumTypeID`) ON DELETE SET NULL,
  CONSTRAINT `FK_album_artist` FOREIGN KEY (`ArtistID`) REFERENCES `artist` (`ArtistID`) ON DELETE CASCADE,
  CONSTRAINT `FK_album_label` FOREIGN KEY (`LabelID`) REFERENCES `label` (`LabelID`) ON DELETE SET NULL,
  CONSTRAINT `FK_album_source` FOREIGN KEY (`SourceID`) REFERENCES `source` (`SourceID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.album: ~0 rows (approximately)
/*!40000 ALTER TABLE `album` DISABLE KEYS */;
/*!40000 ALTER TABLE `album` ENABLE KEYS */;

-- Dumping structure for view catalogue.albumlengths
DROP VIEW IF EXISTS `albumlengths`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `albumlengths` (
	`albumid` INT(11) NOT NULL,
	`albumlength` DECIMAL(32,0) NULL
) ENGINE=MyISAM;

-- Dumping structure for table catalogue.albumtype
DROP TABLE IF EXISTS `albumtype`;
CREATE TABLE IF NOT EXISTS `albumtype` (
  `AlbumTypeID` int(11) NOT NULL AUTO_INCREMENT,
  `AlbumType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`AlbumTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.albumtype: ~9 rows (approximately)
/*!40000 ALTER TABLE `albumtype` DISABLE KEYS */;
REPLACE INTO `albumtype` (`AlbumTypeID`, `AlbumType`) VALUES
	(1, 'Studio'),
	(2, 'Live'),
	(3, 'Single'),
	(4, 'EP'),
	(5, 'Compilation'),
	(6, 'Unofficial'),
	(7, 'Soundtrack'),
	(8, 'Spoken Word'),
	(9, 'Classical'),
	(10, 'Studio + Live'),
	(11, 'Spoken + Studio');
/*!40000 ALTER TABLE `albumtype` ENABLE KEYS */;

-- Dumping structure for table catalogue.artist
DROP TABLE IF EXISTS `artist`;
CREATE TABLE IF NOT EXISTS `artist` (
  `ArtistID` int(11) NOT NULL AUTO_INCREMENT,
  `ArtistName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ArtistID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.artist: ~0 rows (approximately)
/*!40000 ALTER TABLE `artist` DISABLE KEYS */;
/*!40000 ALTER TABLE `artist` ENABLE KEYS */;

-- Dumping structure for view catalogue.chart_album_alltime
DROP VIEW IF EXISTS `chart_album_alltime`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_album_alltime` (
	`albumid` INT(11) NOT NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_album_annual
DROP VIEW IF EXISTS `chart_album_annual`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_album_annual` (
	`y` INT(4) NULL,
	`albumid` INT(11) NOT NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_album_month
DROP VIEW IF EXISTS `chart_album_month`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_album_month` (
	`y` INT(4) NULL,
	`m` INT(2) NULL,
	`albumid` INT(11) NOT NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_album_thisyearsreleases
DROP VIEW IF EXISTS `chart_album_thisyearsreleases`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_album_thisyearsreleases` (
	`y` INT(4) NULL,
	`albumid` INT(11) NOT NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_artist_alltime
DROP VIEW IF EXISTS `chart_artist_alltime`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_artist_alltime` (
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_artist_annual
DROP VIEW IF EXISTS `chart_artist_annual`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_artist_annual` (
	`y` INT(4) NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_artist_month
DROP VIEW IF EXISTS `chart_artist_month`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_artist_month` (
	`y` INT(4) NULL,
	`m` INT(2) NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for view catalogue.chart_ep_annual
DROP VIEW IF EXISTS `chart_ep_annual`;
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `chart_ep_annual` (
	`y` INT(4) NULL,
	`albumid` INT(11) NOT NULL,
	`artistname` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`album` VARCHAR(255) NULL COLLATE 'utf8_general_ci',
	`logtime` DECIMAL(54,0) NULL,
	`logcount` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Dumping structure for table catalogue.label
DROP TABLE IF EXISTS `label`;
CREATE TABLE IF NOT EXISTS `label` (
  `LabelID` int(11) NOT NULL AUTO_INCREMENT,
  `LabelName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`LabelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.label: ~144 rows (approximately)
/*!40000 ALTER TABLE `label` DISABLE KEYS */;
REPLACE INTO `label` (`LabelID`, `LabelName`) VALUES
	(1, 'Go! Discs'),
	(2, 'Utility'),
	(3, 'BBC'),
	(4, 'CBS / Columbia'),
	(5, 'Virgin'),
	(6, 'EMI'),
	(7, 'DJM'),
	(8, 'Portrait'),
	(9, 'WEA'),
	(10, 'EG'),
	(11, 'Charisma'),
	(12, 'A&M'),
	(13, 'Virgin EMI'),
	(14, 'UCJ'),
	(15, 'Mercury'),
	(16, 'Volcano'),
	(17, 'Rock \'n\' Roll'),
	(18, 'RCA'),
	(19, 'Geffen'),
	(20, 'Island'),
	(21, 'Universal'),
	(22, 'Warner Bros.'),
	(23, 'Atco'),
	(24, 'Sky'),
	(25, 'Columbia (EMI)'),
	(26, 'Manhattan'),
	(27, 'Arista'),
	(28, 'InsideOut'),
	(29, 'MCA'),
	(30, 'Philips'),
	(31, 'ClassicFM'),
	(32, 'Rough Trade'),
	(33, 'Vertigo'),
	(34, 'Blue Note'),
	(35, 'Synphara'),
	(36, 'Ricordi'),
	(37, 'Parlophone'),
	(38, 'Epic'),
	(39, 'Laughing Stock'),
	(40, 'Penguin'),
	(41, 'Kscope'),
	(42, 'Sound Entertainment'),
	(43, 'Rykodisc'),
	(44, 'Harvest'),
	(45, 'Spectrum'),
	(46, 'One Little Indian'),
	(47, 'Private Music'),
	(48, 'Warp'),
	(49, '4AD'),
	(50, 'Sire'),
	(51, 'Decca'),
	(52, 'Deram'),
	(53, 'Mute'),
	(54, 'Verve'),
	(55, 'EastWest'),
	(56, 'Magnet'),
	(57, 'Atlantic'),
	(58, 'Varèse Sarabande'),
	(59, 'Deutsche Grammophon'),
	(60, 'Polydor'),
	(61, 'Spotted Peccary'),
	(62, 'Capitol'),
	(63, 'Curtom'),
	(64, 'Nonsuch'),
	(65, 'Venture'),
	(66, '(Self-Released)'),
	(67, 'Capricorn'),
	(68, 'Elektra'),
	(69, 'Roadrunner'),
	(70, 'United Artists'),
	(71, 'Asylum'),
	(72, 'Brain'),
	(73, 'Radar'),
	(74, 'Hip-O'),
	(75, 'Sanctuary'),
	(76, 'Essential'),
	(77, 'Manticore'),
	(78, 'Duck'),
	(79, 'Reprise'),
	(80, 'Wind Up'),
	(81, 'Knitting Factory'),
	(82, 'Dick Bros.'),
	(83, 'Zappa'),
	(84, 'Headform'),
	(85, 'Food for Thought'),
	(86, 'Dark Horse'),
	(87, 'earMusic'),
	(88, 'Constellation'),
	(89, 'Chrysalis'),
	(90, '(No label)'),
	(91, 'Grönland'),
	(92, 'Bounce'),
	(93, 'Samurai'),
	(94, 'Giant Electric Pea'),
	(95, 'Sahara'),
	(96, 'Electronic Sound'),
	(97, 'Third Man'),
	(98, 'groove.nl'),
	(99, 'Moonpop'),
	(100, 'Fontana'),
	(101, 'Erdenklang'),
	(102, 'ZYX'),
	(103, 'U-Vibe'),
	(104, 'Strike Back'),
	(105, 'CBS Masterworks / Sony Classical'),
	(106, 'American Recordings'),
	(107, 'Realworld'),
	(108, 'Yellow'),
	(109, 'RCA Red Seal'),
	(110, 'Kirschner'),
	(111, 'BureauB'),
	(112, 'DGM'),
	(113, 'Gramavision'),
	(114, 'Revisited'),
	(115, 'Sony'),
	(116, 'Warner Music'),
	(117, 'Swan Song'),
	(118, 'Level 42'),
	(119, 'Quinlan Road'),
	(120, 'LSO Live'),
	(121, 'MG.ART'),
	(122, 'Madfish'),
	(123, 'Intact'),
	(124, 'Jive Electro'),
	(125, '10'),
	(126, 'Rubber'),
	(127, 'Little Idiot'),
	(128, 'Wall of Sound'),
	(129, 'Rock Action'),
	(130, 'Barclay'),
	(131, 'Mushroom'),
	(132, 'Radiant'),
	(133, 'Big Brother'),
	(134, 'Nuclear Blast'),
	(135, 'Dovetail'),
	(136, 'Elusive'),
	(137, 'Penguin Café'),
	(138, 'Zopf'),
	(139, 'Face Value'),
	(140, 'Jemp'),
	(141, 'Lava'),
	(142, 'Tonefloat'),
	(143, 'ZTT'),
	(144, 'Fax'),
	(145, 'Test Card'),
	(146, 'Hollywood'),
	(147, 'IRS'),
	(148, 'XL'),
	(149, 'Motor'),
	(150, 'Casablanca'),
	(151, 'All Saints'),
	(152, 'Bon Aire'),
	(153, 'Santana IV');
/*!40000 ALTER TABLE `label` ENABLE KEYS */;

-- Dumping structure for table catalogue.log
DROP TABLE IF EXISTS `log`;
CREATE TABLE IF NOT EXISTS `log` (
  `LogID` int(11) NOT NULL AUTO_INCREMENT,
  `AlbumID` int(11) DEFAULT NULL,
  `LogDate` date DEFAULT NULL,
  PRIMARY KEY (`LogID`),
  KEY `FK__album` (`AlbumID`),
  CONSTRAINT `FK__album` FOREIGN KEY (`AlbumID`) REFERENCES `album` (`AlbumID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.log: ~0 rows (approximately)
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
/*!40000 ALTER TABLE `log` ENABLE KEYS */;

-- Dumping structure for table catalogue.source
DROP TABLE IF EXISTS `source`;
CREATE TABLE IF NOT EXISTS `source` (
  `SourceID` int(11) NOT NULL AUTO_INCREMENT,
  `Source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`SourceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.source: ~4 rows (approximately)
/*!40000 ALTER TABLE `source` DISABLE KEYS */;
REPLACE INTO `source` (`SourceID`, `Source`) VALUES
	(1, 'CD'),
	(2, 'Vinyl'),
	(3, 'Cassette'),
	(4, 'Digital');
/*!40000 ALTER TABLE `source` ENABLE KEYS */;

-- Dumping structure for table catalogue.track
DROP TABLE IF EXISTS `track`;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table catalogue.track: ~0 rows (approximately)
/*!40000 ALTER TABLE `track` DISABLE KEYS */;
/*!40000 ALTER TABLE `track` ENABLE KEYS */;

-- Dumping structure for view catalogue.albumlengths
DROP VIEW IF EXISTS `albumlengths`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `albumlengths`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `albumlengths` AS select `album`.`AlbumID` AS `albumid`,sum(`track`.`Length`) AS `albumlength` from (`album` join `track` on((`album`.`AlbumID` = `track`.`AlbumID`))) where (`track`.`BonusTrack` = 0) group by `album`.`AlbumID` ;

-- Dumping structure for view catalogue.chart_album_alltime
DROP VIEW IF EXISTS `chart_album_alltime`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_album_alltime`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_album_alltime` AS select `album`.`AlbumID` AS `albumid`,`artist`.`ArtistName` AS `artistname`,`album`.`Album` AS `album`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`album`.`ArtistID` = `artist`.`ArtistID`))) where (`album`.`AlbumTypeID` not in (3,4,6,8)) group by `artist`.`ArtistName`,`album`.`Album` order by sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_album_annual
DROP VIEW IF EXISTS `chart_album_annual`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_album_annual`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_album_annual` AS select year(`log`.`LogDate`) AS `y`,`album`.`AlbumID` AS `albumid`,`artist`.`ArtistName` AS `artistname`,`album`.`Album` AS `album`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`album`.`ArtistID` = `artist`.`ArtistID`))) where (`album`.`AlbumTypeID` not in (3,4,6,8)) group by year(`log`.`LogDate`),`artist`.`ArtistName`,`album`.`Album` order by year(`log`.`LogDate`),sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_album_month
DROP VIEW IF EXISTS `chart_album_month`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_album_month`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_album_month` AS select year(`log`.`LogDate`) AS `y`,month(`log`.`LogDate`) AS `m`,`album`.`AlbumID` AS `albumid`,`artist`.`ArtistName` AS `artistname`,`album`.`Album` AS `album`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`album`.`ArtistID` = `artist`.`ArtistID`))) where (`album`.`AlbumTypeID` not in (3,4,6,8)) group by year(`log`.`LogDate`),month(`log`.`LogDate`),`artist`.`ArtistName`,`album`.`Album` order by year(`log`.`LogDate`),month(`log`.`LogDate`),sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_album_thisyearsreleases
DROP VIEW IF EXISTS `chart_album_thisyearsreleases`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_album_thisyearsreleases`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `chart_album_thisyearsreleases` AS select 	year(`log`.`LogDate`) AS `y`,
			`album`.`AlbumID` AS `albumid`,
			`artist`.`ArtistName` AS `artistname`,
			`album`.`Album` AS `album`,
			sum(`albumlengths`.`albumlength`) AS `logtime`,
			count(`log`.`LogID`) AS `logcount` 
from 		(((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) 
			join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) 
			join `artist` on((`album`.`ArtistID` = `artist`.`ArtistID`))) 
where (`album`.`AlbumTypeID` not in (3,4,6,8)) and `album`.YearReleased = year(`log`.`logdate`)
group by year(`log`.`LogDate`),`artist`.`ArtistName`,`album`.`Album` order by year(`log`.`LogDate`),sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_artist_alltime
DROP VIEW IF EXISTS `chart_artist_alltime`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_artist_alltime`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_artist_alltime` AS select `artist`.`ArtistName` AS `artistname`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`artist`.`ArtistID` = `album`.`ArtistID`))) where (`album`.`AlbumTypeID` not in (6,8)) group by `artist`.`ArtistName` order by sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_artist_annual
DROP VIEW IF EXISTS `chart_artist_annual`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_artist_annual`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_artist_annual` AS select year(`log`.`LogDate`) AS `y`,`artist`.`ArtistName` AS `artistname`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`artist`.`ArtistID` = `album`.`ArtistID`))) where (`album`.`AlbumTypeID` not in (6,8)) group by year(`log`.`LogDate`),`artist`.`ArtistName` order by year(`log`.`LogDate`),sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_artist_month
DROP VIEW IF EXISTS `chart_artist_month`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_artist_month`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_artist_month` AS select year(`log`.`LogDate`) AS `y`,month(`log`.`LogDate`) AS `m`,`artist`.`ArtistName` AS `artistname`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`artist`.`ArtistID` = `album`.`ArtistID`))) where (`album`.`AlbumTypeID` not in (6,8)) group by year(`log`.`LogDate`),month(`log`.`LogDate`),`artist`.`ArtistName` order by year(`log`.`LogDate`),month(`log`.`LogDate`),sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

-- Dumping structure for view catalogue.chart_ep_annual
DROP VIEW IF EXISTS `chart_ep_annual`;
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `chart_ep_annual`;
CREATE ALGORITHM=UNDEFINED DEFINER=`simon`@`localhost` VIEW `chart_ep_annual` AS select year(`log`.`LogDate`) AS `y`,`album`.`AlbumID` AS `albumid`,`artist`.`ArtistName` AS `artistname`,`album`.`Album` AS `album`,sum(`albumlengths`.`albumlength`) AS `logtime`,count(`log`.`LogID`) AS `logcount` from (((`albumlengths` join `album` on((`albumlengths`.`albumid` = `album`.`AlbumID`))) join `log` on((`log`.`AlbumID` = `album`.`AlbumID`))) join `artist` on((`album`.`ArtistID` = `artist`.`ArtistID`))) where (`album`.`AlbumTypeID` = 4) group by year(`log`.`LogDate`),`artist`.`ArtistName`,`album`.`Album` order by year(`log`.`LogDate`),sum(`albumlengths`.`albumlength`) desc,count(`log`.`LogID`) desc ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
