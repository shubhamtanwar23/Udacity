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

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    QUERY = "SELECT count(*) FROM player;"
    cursor.execute(QUERY)
    count = cursor.fetchone()[0]
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
    QUERY = "CREATE VIEW view_wins as "\
            "SELECT player.id, count(matches.id) as wins "\
            "FROM player left outer join matches ON player.id=matches.winner "\
            "GROUP BY player.id;"
    cursor.execute(QUERY)
    QUERY = "CREATE VIEW view_played as "\
            "SELECT player.id, count(matches.id) as played "\
            "FROM player left outer join matches ON player.id=matches.winner "\
            "or player.id=matches.loser GROUP BY player.id;"
    cursor.execute(QUERY)
    QUERY = "SELECT player.id, player.name, view_wins.wins, view_played.played "\
            "FROM player INNER JOIN view_wins ON player.id=view_wins.id "\
            "INNER JOIN view_played ON player.id=view_played.id ORDER BY view_wins.wins;"
    cursor.execute(QUERY)
    result = cursor.fetchall()
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
    QUERY = "INSERT INTO matches(winner, loser) VALUES(%s, %s);"
    cursor.execute(QUERY, (winner,loser,))
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
    standings = playerStandings()
    total_player = len(standings)
    rows = []
    i = 0
    while i < total_player: 
        pair = (standings[i][0],standings[i][1],standings[i+1][0],standings[i+1][1])
        rows.append(pair)
        i += 2
    return rows
