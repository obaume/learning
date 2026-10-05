import sportsdataverse as sdv
import sportsdataverse.nhl as nhl
import pandas as pd

def safe(label, thunk):
    try:
        out = thunk()
        print(f'✅ {label}')
        return out
    except Exception as e:
        print(f'⏭️  {label}: unavailable right now ({type(e).__name__})')
        return None
def get_standing():
    standings = safe('native standings', lambda: nhl.nhl_standings(date="2026-04-17"))
    if standings is not None:
        out = (standings.select(['team_name_default', 'goal_for', 'goal_against', 'win_pctg',  'points'])
            .sort('points', descending=True))
    return out

def pythagorean(y, x):
    return 0

standing = get_standing()

score_ratio = (standing.get_column('goal_for') / standing.get_column('goal_against')).alias('score_ratio')
standing.insert_column(5,score_ratio)

pyth_pct = (1 / (1 + standing.get_column('score_ratio') ** -2)).alias('pyth_pct')
standing.insert_column(6, pyth_pct)

pyth_err = ((standing.get_column('win_pctg') - standing.get_column('pyth_pct')) ** 2).alias('pyth_err')
standing.insert_column(7, pyth_err)

print(standing.sort('pyth_err', descending=True).head())
print(standing.sort('pyth_err', descending=False).head())
