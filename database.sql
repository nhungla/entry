create database entry_task;
use entry_task;

create table event_tab(
	id int(64) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	create_uid int(32) UNSIGNED,
	create_time int(32) UNSIGNED,
	start_time int(32) UNSIGNED,
	end_time int(32) UNSIGNED,
	channel int(8) UNSIGNED,
	extra_data text,
	INDEX idx_channel_end_time_start_time(channel, end_time, start_time)
);

create table user_tab (
	id int(64) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	user_name varchar(255),
	salt varchar(20),
	password_hash varchar(255),
	user_type int(8) UNSIGNED,
    UNIQUE INDEX idx_user_name(user_name)
);

create table event_participant_tab (
	id int(64) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	user_id int(64) UNSIGNED,
	event_id int(64) UNSIGNED,
	UNIQUE INDEX idx_event_id_user_id(event_id, user_id)
);

create table event_like_tab (
	id int(64) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	user_id int(64) UNSIGNED,
	event_id int(64) UNSIGNED,
	UNIQUE INDEX idx_event_id_user_id(event_id, user_id)
);

create table event_comment_tab (
	id int(64) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	user_id int(64) UNSIGNED,
	event_id int(64) UNSIGNED,
	extra_data text,
	INDEX idx_event_id(event_id)
);
