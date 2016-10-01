CREATE DATABASE bilibili_users;
USE bilibili_users;
CREATE TABLE `bilibili_user_info` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `mid` varchar(11) DEFAULT NULL,
    `name` varchar(100) DEFAULT NULL,
    `sex` varchar(11) DEFAULT NULL,
    `face` varchar(500) DEFAULT NULL,
    `coins` int(11) DEFAULT NULL,
    `regtime` varchar(50) DEFAULT NULL,
    `spacesta` int(11) DEFAULT NULL,
    `birthday` varchar(50) DEFAULT NULL,
    `place` varchar(100) DEFAULT NULL,
    `description` varchar(200) DEFAULT NULL,
    `article` int(11) DEFAULT NULL,
    `attentions` text DEFAULT NULL,
    `fans` int(11) DEFAULT NULL,
    `friend` int(11) DEFAULT NULL,
    `attention` int(11) DEFAULT NULL,
    `sign` varchar(500) DEFAULT NULL,
    `li_current_level` int(11)  DEFAULT NULL,
    `li_current_min` int(11) DEFAULT NULL,
    `li_current_exp` int(11) DEFAULT NULL,
    `li_next_exp` int(11) DEFAULT NULL,
    `playNum` int(11) DEFAULT NULL,
    PRIMARY KEY(`id`)
)CHARSET=utf8;
