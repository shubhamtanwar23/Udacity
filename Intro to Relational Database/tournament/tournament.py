#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(dbname="tournament", user="shubham", password="shubh23")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "DELETE FROM matches;"
    cursor.execute(QUERY)
    QUERY = "UPDATE player SET wins=0, matches=0;"
    cursor.execute(QUERY)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "DELETE FROM player;"
    cursor.execute(QUERY)
    conn.commit()
    conn.close()
    deleteMatches()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "SELECT count(*) FROM player;"
    cursor.execute(QUERY)
    count = cursor.fetchall()[0][0]
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = "INSERT INTO player(name) VALUES(%s);"
    cursor.execute(QUERY, (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = "SELECT * FROM player ORDER BY wins desc;"
    cursor.execute(QUERY)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = "UPDATE player SET wins = wins + 1, matches = matches + 1 where id=%s;"
    cursor.execute(QUERY, (winner,))
    QUERY = "UPDATE player SET matches = matches + 1 where id=%s;"
    cursor.execute(QUERY, (loser,))
    conn.commit()
    QUERY = "UPDATE matches SET winner =(SELECT name FROM player WHERE id=%s) "\
            "where (id1=%s and id2=%s) OR (id2=%s and id1=%s);"
    cursor.execute(QUERY, (winner,winner,loser,winner,loser))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = "SELECT id, name FROM player order by wins;"
    cursor.execute(QUERY)
    id_name = cursor.fetchall()
    total_player = len(id_name)
    rows = []
    i = 0
    while i < total_player: 
        QUERY_MATCH = "INSERT INTO matches(id1,name1,id2,name2) VALUES(%s,%s,%s,%s);"
        pair = [(id_name[i][0],id_name[i][1],id_name[i+1][0],id_name[i+1][1]),]
        rows += pair
        cursor.execute(QUERY_MATCH,(id_name[i][0],id_name[i][1],id_name[i+1][0],id_name[i+1][1],))
        i += 2
    conn.commit()
    conn.close()
    return rows
