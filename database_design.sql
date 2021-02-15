-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema learners
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema learners
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `learners` DEFAULT CHARACTER SET utf8 ;
USE `learners` ;

-- -----------------------------------------------------
-- Table `learners`.`assess_modality`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learners`.`assess_modality` (
  `modality_id` INT(11) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`modality_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `learners`.`current_learner`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `learners`.`current_learner` (
  `entry_id` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `form` VARCHAR(4) NOT NULL,
  `module` VARCHAR(4) NOT NULL,
  `score` DECIMAL(4,1) NOT NULL,
  `level` VARCHAR(50) NOT NULL,
  `modality_id` INT(11) NOT NULL,
  `student_id` VARCHAR(50) NOT NULL,
  `hours` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`entry_id`, `modality_id`),
  INDEX `fk_current_learner_assess_modality_idx` (`modality_id` ASC),
  CONSTRAINT `fk_current_learner_assess_modality`
    FOREIGN KEY (`modality_id`)
    REFERENCES `learners`.`assess_modality` (`modality_id`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

