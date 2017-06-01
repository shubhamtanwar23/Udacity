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
name	text);


-- matches TABLE which stores information about the matches(pairing) and winner of it
CREATE TABLE matches(
id	serial	primary key,
winner	integer	references	player(id),
loser	integer	references	player(id));