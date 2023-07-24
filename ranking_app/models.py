from django.db import models

# Create your models here.
POSITIONS = (
    ('QB', 'QuarterBack'),
    ('RB', 'RunningBack'),
    ('WR', 'WideReceiver'),
    ('TE', 'TightEnd'),
    ('DEF', 'Defense'),
    ('K', 'Kicker'),
)

SCORING_TYPES = (
    ('STANDARD', 'STANDARD'),
    ('PPR', 'PPR')
)

TEAMS = (
    ('ARZ', 'Arizona Cardinals'),
    ('ATL', 'Atlanta Falcons'),
    ('BAL', 'Baltimore Ravens'),
    ('BUF', 'Buffalo Bills'),
    ('CAR', 'Carolina Panthers'),
    ('CHI', 'Chicago Bears'),
    ('CIN', 'Cincinnati Bengals'),
    ('CLE', 'Cleveland Browns'),
    ('DAL', 'Dallas Cowboys'),
    ('DEN', 'Denver Broncos'),
    ('DET', 'Detroit Lions'),
    ('GB', 'Green Bay Packers'),
    ('HOU', 'Houson Texans'),
    ('IND', 'Indianapolis Colts'),
    ('JAX', 'Jacksonville Jaguars'),
    ('KC', 'Kansas City Chiefs'),
    ('LV', 'Las Vegas Raiders'),
    ('LAC', 'Los Angeles Chargers'),
    ('LAR', 'Los Angeles Rams'),
    ('MIA', 'Miami Dolphins'),
    ('MIN', 'Minnesota Vikings'),
    ('NE', 'New England Patriots'),
    ('NO', 'New Orleans Saints'),
    ('NYG', 'New York Giants'),
    ('NYJ', 'New York Jets'),
    ('PHI', 'Philadelphia Eagles'),
    ('PIT', 'Pittsburgh Steelers'),
    ('SF', 'San Francisco 49ers'),
    ('SEA', 'Seattle Seahawks'),
    ('TB', 'Tampa Bay Buccaneers'),
    ('TEN', 'Tennessee Titans'),
    ('WAS', 'Washington Commanders'),
    ('FA', 'Free Agent')
)

class Player(models.Model):
    player_name = models.CharField(max_length=30)
    position = models.CharField(max_length=3, choices=POSITIONS)
    team = models.CharField(max_length=3, choices=TEAMS)
    bye_week = models.IntegerField()

class RankingSource(models.Model):
    ranking_src_name = models.CharField(max_length=30)
    ranking_src_url = models.TextField()
    date = models.DateField()
    scoring_type = models.CharField(max_length=10, choices=SCORING_TYPES)
    players_count = models.IntegerField()

class Ranking(models.Model):
    ranking_src = models.ForeignKey(RankingSource, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rank = models.IntegerField()
