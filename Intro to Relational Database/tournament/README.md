# Udacity Intro To Relational Database
This a final project for the course.

In this a databse is created for a tournament with swiss pairing. 

### Dependencies
1. Postgresql Database Server for maintaining database
2. psycopg2 DB-API 



### tournament.sql
This file contains the create query for two tables i.e player and matches.



### tournament.py 
This file contain various functions for accesing information from the database.

|	Functions |	Description |
| ------ | ------ |
| connect() |	Meant to connect to the database. |
| deleteMatches() |	Remove all the matches records from the database. |
| deletePlayers() |	Remove all the players records from the database. |
| countPlayers()	|	Return the number of player currently registered. |
| registerPlayers(name) |	Adds a player name to the tournament database. |
| playerStandings |	Return a list of player and their wins records sorted by win. |
| reportMatch(winner,loser) |	Populates the matches table and record the winner and loser. |
| swissPairings() |	Returns a list of pairs of players for the next round of match. |



### tournament_test.py
It contains various function for unit testing. 
