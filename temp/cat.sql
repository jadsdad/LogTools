-- --------------------------------------------------------
-- host:                         127.0.0.1
-- server version:               10.2.9-mariadb - mariadb.org binary distribution
-- server os:                    win64
-- heidisql version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 set @old_character_set_client=@@character_set_client */;
/*!40101 set names utf8 */;
/*!50503 set names utf8mb4 */;
/*!40014 set @old_foreign_key_checks=@@foreign_key_checks, foreign_key_checks=0 */;
/*!40101 set @old_sql_mode=@@sql_mode, sql_mode='no_auto_value_on_zero' */;

-- dumping structure for view catalogue.chart_album_annual
-- removing temporary table and create final view structure
drop table if exists `chart_album_annual`;
create view `chart_album_annual` as select 		year(log.logdate) as y, 
				artist.artistname, 
				album.album, 
				sum(albumlengths.albumlength) as logtime, 
				count(log.logid) as logcount

from 			albumlengths 
					inner join album on albumlengths.albumid = album.albumid
					inner join log on log.albumid = album.albumid
					inner join artist on album.artistid = artist.artistid
					
where			album.albumtypeid not in (3, 4, 8)
group by		y, artist.artistname, album.album
order by		y, logtime desc, logcount desc ;

-- dumping structure for view catalogue.chart_album_month
-- removing temporary table and create final view structure
drop table if exists `chart_album_month`;
create view `chart_album_month` as select 		year(log.logdate) as y, 
				month(log.logdate) as m,
				artist.artistname, 
				album.album, 
				sum(albumlengths.albumlength) as logtime, 
				count(log.logid) as logcount

from 			albumlengths 
					inner join album on albumlengths.albumid = album.albumid
					inner join log on log.albumid = album.albumid
					inner join artist on album.artistid = artist.artistid
					
where			album.albumtypeid not in (3, 4, 8)
group by		y, m, artist.artistname, album.album
order by		y, m, logtime desc, logcount desc ;

-- dumping structure for view catalogue.chart_artist_annual
-- removing temporary table and create final view structure
drop table if exists `chart_artist_annual`;
create view `chart_artist_annual` as select 		year(log.logdate) as y, 
				artist.artistname, 
				sum(albumlengths.albumlength) as logtime, 
				count(log.logid) as logcount

from 			albumlengths 
					inner join album on albumlengths.albumid = album.albumid
					inner join log on log.albumid = album.albumid
					inner join artist on artist.artistid = album.artistid					
where			album.albumtypeid not in (3, 4, 8)
group by		y, artist.artistname
order by		y, logtime desc, logcount desc ;

-- dumping structure for view catalogue.chart_artist_month
-- removing temporary table and create final view structure
drop table if exists `chart_artist_month`;
create view `chart_artist_month` as select 		year(log.logdate) as y, 
				month(log.logdate) as m,
				artist.artistname, 
				sum(albumlengths.albumlength) as logtime, 
				count(log.logid) as logcount

from 			albumlengths 
					inner join album on albumlengths.albumid = album.albumid
					inner join log on log.albumid = album.albumid
					inner join artist on artist.artistid = album.artistid					
where			album.albumtypeid not in (3, 4, 8)
group by		y, m, artist.artistname
order by		y, m, logtime desc, logcount desc ;

/*!40101 set sql_mode=ifnull(@old_sql_mode, '') */;
/*!40014 set foreign_key_checks=if(@old_foreign_key_checks is null, 1, @old_foreign_key_checks) */;
/*!40101 set character_set_client=@old_character_set_client */;
