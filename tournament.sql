-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


DROP TABLE IF EXISTS players;
-- Registered players
CREATE TABLE players (
	id	serial	PRIMARY KEY, 
	name	varchar(40) NOT NULL
);


DROP TABLE IF EXISTS matches;
-- Assignemnt of matches between players and the outcome
CREATE TABLE matches (
	player1	integer,
	player2 integer,
	winner	integer NOT NULL
);


DROP VIEW IF EXISTS matches_played;
-- Create View for number of matches played for each player
CREATE VIEW matches_played AS
SELECT id, name, COUNT(players.id) AS played
    FROM Players, Matches
    WHERE Players.id = Matches.player1 OR Players.id = Matches.player2
    GROUP BY id 
    ORDER BY played DESC;


DROP VIEW IF EXISTS number_of_wins;
-- Create view for number of wins for each player
CREATE VIEW number_of_wins AS
  SELECT id, COUNT(matches.winner) AS wins
  FROM Matches, Players
  WHERE Players.id = Matches.winner
  GROUP BY id
  ORDER BY wins DESC;


DROP VIEW IF EXISTS standings;
-- View of player standings as matches are played in the tournament 
CREATE VIEW standings AS 
	SELECT p.id, p.name, 
	case when w.wins is null then 0 else wins end, 
	case when m.played is null then 0 else played end 
	FROM players p LEFT JOIN number_of_wins w ON p.id=w.id 
	LEFT JOIN matches_played m ON p.id=m.id 
	ORDER BY w.wins

