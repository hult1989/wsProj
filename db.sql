-- MySQL dump 10.13  Distrib 5.6.25, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: wsdb
-- ------------------------------------------------------
-- Server version	5.6.25-0ubuntu0.15.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `imei` varchar(20) DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `imei` (`imei`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES ('123456789abcedf0',-23.12321,87.22234,'2015-09-30 06:12:23'),('1024',-12.3433,33.123,'2015-09-23 04:34:12'),('1024',-12.3433,33.123,'2015-09-21 04:34:12'),('1024',-12.3433,44.123,'2015-09-29 04:34:12');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sosnumber`
--

DROP TABLE IF EXISTS `sosnumber`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sosnumber` (
  `imei` varchar(20) DEFAULT NULL,
  `sosnumber` varchar(20) DEFAULT NULL,
  `contact` varchar(30) DEFAULT NULL,
  UNIQUE KEY `imei` (`imei`,`sosnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sosnumber`
--

LOCK TABLES `sosnumber` WRITE;
/*!40000 ALTER TABLE `sosnumber` DISABLE KEYS */;
INSERT INTO `sosnumber` VALUES ('1024','13836435683','alice'),('1024','13836435684','bob');
/*!40000 ALTER TABLE `sosnumber` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_sos`
--

DROP TABLE IF EXISTS `temp_sos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temp_sos` (
  `imei` varchar(20) DEFAULT NULL,
  `sosnumber` varchar(20) DEFAULT NULL,
  `contact` varchar(30) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `imei` (`imei`,`sosnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_sos`
--

LOCK TABLES `temp_sos` WRITE;
/*!40000 ALTER TABLE `temp_sos` DISABLE KEYS */;
INSERT INTO `temp_sos` VALUES ('1024','+8615652963154','è¶…äºº','2015-10-05 06:09:09'),('123456789abcdef0','15882205392','cathy','2015-10-05 14:10:56'),('1024','13456412345','\\u8d85\\u4eba','2015-10-06 12:26:41');
/*!40000 ALTER TABLE `temp_sos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_user_ws`
--

DROP TABLE IF EXISTS `temp_user_ws`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temp_user_ws` (
  `simnum` varchar(20) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`simnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_user_ws`
--

LOCK TABLES `temp_user_ws` WRITE;
/*!40000 ALTER TABLE `temp_user_ws` DISABLE KEYS */;
INSERT INTO `temp_user_ws` VALUES ('13836435682','alice','2015-10-06 11:28:19');
/*!40000 ALTER TABLE `temp_user_ws` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_ws`
--

DROP TABLE IF EXISTS `user_ws`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_ws` (
  `username` varchar(50) DEFAULT NULL,
  `imei` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `isdefault` char(1) DEFAULT NULL,
  UNIQUE KEY `username` (`username`,`imei`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_ws`
--

LOCK TABLES `user_ws` WRITE;
/*!40000 ALTER TABLE `user_ws` DISABLE KEYS */;
INSERT INTO `user_ws` VALUES ('alice','3','hulk','1'),('alice','1','superman1','1'),('alice','2','superman2','1'),('alice','4','superman4','1'),('hulk','98789',NULL,'1'),('alice','2046',NULL,'1'),('hulk','123456789abcedf0',NULL,'1');
/*!40000 ALTER TABLE `user_ws` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userinfo` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinfo`
--

LOCK TABLES `userinfo` WRITE;
/*!40000 ALTER TABLE `userinfo` DISABLE KEYS */;
INSERT INTO `userinfo` VALUES ('alice','newpassword',NULL,NULL,NULL),('batman',NULL,NULL,'batman@jla',NULL),('superman','nicai',NULL,NULL,'2015-10-06'),('uperman','nicai',NULL,NULL,'2015-10-06'),('xmen','15882205392',NULL,NULL,'2015-10-05');
/*!40000 ALTER TABLE `userinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(245) DEFAULT NULL,
  `last_name` varchar(233) DEFAULT NULL,
  `age` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'hao','tang',26),(2,'alice','dan',23);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wsinfo`
--

DROP TABLE IF EXISTS `wsinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wsinfo` (
  `imei` varchar(20) NOT NULL,
  `imsi` varchar(20) DEFAULT NULL,
  `simnum` varchar(20) DEFAULT NULL,
  `adminpwd` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`imei`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wsinfo`
--

LOCK TABLES `wsinfo` WRITE;
/*!40000 ALTER TABLE `wsinfo` DISABLE KEYS */;
INSERT INTO `wsinfo` VALUES ('1024','','10086','123456'),('123456789abcedf0','','15882205392','123456'),('1984',NULL,NULL,'123456'),('2046','','15652963154','123456'),('2048','1234','13836435683','123456'),('22','33','123456','123456'),('98789','','10086','123456');
/*!40000 ALTER TABLE `wsinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-10-07  9:47:11
