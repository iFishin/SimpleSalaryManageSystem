/*
 Navicat Premium Data Transfer

 Source Server         : 本地服务器
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : employees

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 31/05/2023 15:14:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `account` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('Administor', 'admin');
INSERT INTO `admin` VALUES ('test', 'test');

-- ----------------------------
-- Table structure for employee_info
-- ----------------------------
DROP TABLE IF EXISTS `employee_info`;
CREATE TABLE `employee_info`  (
  `employee_id` int NOT NULL,
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `age` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `unit` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `position` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `salary` float NULL DEFAULT 0,
  PRIMARY KEY (`employee_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of employee_info
-- ----------------------------
INSERT INTO `employee_info` VALUES (10001, 'Fish', 'male', '99', '经理室', 'boss', 9600);
INSERT INTO `employee_info` VALUES (10002, 'CatFish', 'female', '18', '财务科', '技术员工', 5700);
INSERT INTO `employee_info` VALUES (10003, 'SillyFish', 'female', '6', '财务科', '技术员工', 4000);
INSERT INTO `employee_info` VALUES (10004, 'GoldFish', 'female', '8', '技术科', '销售员工', 6100);
INSERT INTO `employee_info` VALUES (10005, 'Lisa', 'female', '17', '技术科', '管理员工', 5100);
INSERT INTO `employee_info` VALUES (10006, '李华', 'male', '56', '销售科', '财务员工', 8000);
INSERT INTO `employee_info` VALUES (10007, '闲散人员1号', 'male', '10', '摸鱼部', '摸鱼达人', 0);
INSERT INTO `employee_info` VALUES (10008, '闲散人员2号', 'female', '10', '池中鱼', '无所事事', 1);

-- ----------------------------
-- Table structure for salary_info
-- ----------------------------
DROP TABLE IF EXISTS `salary_info`;
CREATE TABLE `salary_info`  (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `basical_salary` float NULL DEFAULT 0,
  `welfare` float NULL DEFAULT 0,
  `award` float NULL DEFAULT 0,
  `unemployment_insurance` float NULL DEFAULT 0,
  `housing_provident_fund` float NULL DEFAULT 0,
  `salary` float NULL DEFAULT 0,
  PRIMARY KEY (`employee_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10009 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of salary_info
-- ----------------------------
INSERT INTO `salary_info` VALUES (10001, 9000, 500, 400, 200, 100, 9600);
INSERT INTO `salary_info` VALUES (10002, 5000, 500, 500, 100, 200, 5700);
INSERT INTO `salary_info` VALUES (10003, 5000, 100, 0, 500, 600, 4000);
INSERT INTO `salary_info` VALUES (10004, 6000, 100, 0, 0, 0, 6100);
INSERT INTO `salary_info` VALUES (10005, 4500, 300, 600, 200, 100, 5100);
INSERT INTO `salary_info` VALUES (10006, 8000, 0, 0, 0, 0, 8000);
INSERT INTO `salary_info` VALUES (10007, 0, 0, 0, 0, 0, 0);
INSERT INTO `salary_info` VALUES (10008, 1, 0, 0, 0, 0, 1);

-- ----------------------------
-- View structure for em_info
-- ----------------------------
DROP VIEW IF EXISTS `em_info`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `em_info` AS select `e`.`employee_id` AS `employee_id`,`e`.`name` AS `name`,`e`.`sex` AS `sex`,`e`.`age` AS `age`,`e`.`unit` AS `unit`,`e`.`position` AS `position`,`s`.`salary` AS `salary`,`s`.`basical_salary` AS `basical_salary`,`s`.`welfare` AS `welfare`,`s`.`award` AS `award`,`s`.`unemployment_insurance` AS `unemployment_insurance`,`s`.`housing_provident_fund` AS `housing_provident_fund` from (`employee_info` `e` join `salary_info` `s`) where (`e`.`employee_id` = `s`.`employee_id`);

-- ----------------------------
-- Procedure structure for account_judge
-- ----------------------------
DROP PROCEDURE IF EXISTS `account_judge`;
delimiter ;;
CREATE PROCEDURE `account_judge`(IN account VARCHAR(20), IN password VARCHAR(20))
BEGIN 
DECLARE result INT; 
SELECT COUNT(*) INTO result 
FROM admin 
WHERE admin.account = account AND admin.password = password; SELECT IF(result>0,1,0); 
END
;;
delimiter ;

-- ----------------------------
-- Function structure for total_em
-- ----------------------------
DROP FUNCTION IF EXISTS `total_em`;
delimiter ;;
CREATE FUNCTION `total_em`()
 RETURNS int
BEGIN 

DECLARE sum INT DEFAULT 0; SELECT COUNT(*) INTO sum FROM employee_info; 
RETURN sum; 

END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table employee_info
-- ----------------------------
DROP TRIGGER IF EXISTS `data_input`;
delimiter ;;
CREATE TRIGGER `data_input` AFTER INSERT ON `employee_info` FOR EACH ROW begin  

insert into salary_info(employee_id,salary) values (new.employee_id,new.salary); 
end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table employee_info
-- ----------------------------
DROP TRIGGER IF EXISTS `data_delete`;
delimiter ;;
CREATE TRIGGER `data_delete` AFTER DELETE ON `employee_info` FOR EACH ROW BEGIN  

DELETE FROM salary_info WHERE employee_id = old.employee_id LIMIT 1; 
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table employee_info
-- ----------------------------
DROP TRIGGER IF EXISTS `data_update`;
delimiter ;;
CREATE TRIGGER `data_update` AFTER UPDATE ON `employee_info` FOR EACH ROW BEGIN 
    UPDATE salary_info 
    SET salary_info.salary = new.salary 
    WHERE salary_info.employee_id = new.employee_id; 
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
