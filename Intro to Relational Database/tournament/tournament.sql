-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.




-- player TABLE which stores the information for registered players
CREATE TABLE player (
id 	serial	 primary key,
name	varchar(20),
wins	smallint	DEFAULT 0,
matches	smallint	DEFAULT 0);


-- matches TABLE which stores information about the matches(pairing) and winner of it
CREATE TABLE matches(
id1	smallint	references	player(id),
name1	varchar(20),
id2	smallint	references	player(id),
name2	varchar(20),
winner	varchar(20));