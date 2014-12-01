DROP TABLE IF EXISTS `SensorValue`;
CREATE TABLE `SensorValue` (
    `Ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Light` FLOAT NOT NULL DEFAULT 0.0,
    `Temperature` FLOAT NOT NULL DEFAULT 0.0,
    PRIMARY KEY (`Ts`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

