#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    result = c.fetchone()
    db.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    # Sanitize output using Bleach to prevent Script Injection attacks
    clean_name = bleach.clean(name)

    # Formatted to prevent SQL Injection attacks
    # if names are entered from web form
    c.execute("INSERT INTO players (name) VALUES (%s)", (clean_name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()

    c.execute("SELECT p.id, p.name, \
        case when w.wins is null then 0 else wins end, \
        case when m.played is null then 0 else played end \
        FROM players p LEFT JOIN number_of_wins w ON p.id=w.id \
        LEFT JOIN matches_played m ON p.id=m.id \
        ORDER BY w.wins")

    result = c.fetchall()
    db.commit()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    # Record the assignment of matches and winner of the match
    c.execute("INSERT INTO matches (player1, player2, winner) \
        VALUES (%s, %s, %s)", (winner, loser, winner))
    db.commit()
    db.close()


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
    db = connect()
    c = db.cursor()

    c.execute("SELECT DISTINCT s1.id, s1.name, s2.id, s2.name \
        FROM standings s1, standings s2 \
        WHERE s1.wins=s2.wins \
        and s1.id<s2.id")

    result = c.fetchall()
    db.commit()
    db.close()
    return result
