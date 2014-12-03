DROP TABLE IF EXISTS `SensorImmediatelyValue`;
CREATE TABLE `SensorImmediatelyValue` (
    `Time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Switch` INTEGER NOT NULL DEFAULT 0,
    `Light` FLOAT NOT NULL DEFAULT 0.0,
    `Temperature` FLOAT NOT NULL DEFAULT 0.0,
    `HumanBody` INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (`Time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO SensorImmediatelyValue VALUES(NULL, 1, 0, 0, 0);
