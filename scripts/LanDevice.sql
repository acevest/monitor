DROP TABLE IF EXISTS `Devices`;
CREATE TABLE `Devices` (
    `MacAddr` char(32) NOT NULL,
    `Name` char(255) NOT NULL,
    `State` FLOAT NOT NULL DEFAULT 0.0,
    `Notify` int(11) NOT NULL DEFAULT '1',
    `Ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`MacAddr`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

