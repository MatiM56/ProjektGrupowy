-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: projekt
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Fingerprints`
--

DROP TABLE IF EXISTS `Fingerprints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fingerprints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `point_id` int DEFAULT NULL,
  `measured_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `raw_data` longblob,
  PRIMARY KEY (`id`),
  KEY `point_id` (`point_id`),
  CONSTRAINT `Fingerprints_ibfk_1` FOREIGN KEY (`point_id`) REFERENCES `tabela_pomiaru` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Pokoj`
--

DROP TABLE IF EXISTS `Pokoj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pokoj` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RadioMap`
--

DROP TABLE IF EXISTS `RadioMap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RadioMap` (
  `id` int NOT NULL AUTO_INCREMENT,
  `point_id` int DEFAULT NULL,
  `bssid` varchar(20) NOT NULL,
  `ssid` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `point_id` (`point_id`),
  KEY `bssid` (`bssid`),
  CONSTRAINT `RadioMap_ibfk_1` FOREIGN KEY (`point_id`) REFERENCES `tabela_pomiaru` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabela_pomiaru`
--

DROP TABLE IF EXISTS `tabela_pomiaru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tabela_pomiaru` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_pokoju` int DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_pokoju` (`id_pokoju`),
  CONSTRAINT `tabela_pomiaru_ibfk_1` FOREIGN KEY (`id_pokoju`) REFERENCES `Pokoj` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-15 13:46:28
