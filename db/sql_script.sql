-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema twitter
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema twitter
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `twitter` DEFAULT CHARACTER SET utf8 ;
USE `twitter` ;

-- -----------------------------------------------------
-- Table `twitter`.`Hashtags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `twitter`.`Hashtags` (
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `twitter`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `twitter`.`Users` (
  `idUsers` BIGINT(20) NOT NULL,
  `username` VARCHAR(45) NULL,
  `followers` INT NULL,
  PRIMARY KEY (`idUsers`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `twitter`.`Tweets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `twitter`.`Tweets` (
  `idTweets` BIGINT(20) NOT NULL,
  `language` VARCHAR(45) NULL,
  `text` TEXT NULL,
  `date` DATETIME NULL,
  `Hashtags_name` VARCHAR(45) NOT NULL,
  `Users_idUsers` BIGINT(20) NOT NULL,
  PRIMARY KEY (`idTweets`, `Hashtags_name`, `Users_idUsers`),
  INDEX `fk_Tweets_Hashtags_idx` (`Hashtags_name` ASC),
  INDEX `fk_Tweets_Users1_idx` (`Users_idUsers` ASC),
  CONSTRAINT `fk_Tweets_Hashtags`
    FOREIGN KEY (`Hashtags_name`)
    REFERENCES `twitter`.`Hashtags` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tweets_Users1`
    FOREIGN KEY (`Users_idUsers`)
    REFERENCES `twitter`.`Users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
