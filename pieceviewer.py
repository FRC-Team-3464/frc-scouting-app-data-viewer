from bokeh.io import show, curdoc
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.layouts import column
from bokeh.themes import Theme, built_in_themes
import json
import random
from bokeh.models import HTMLTemplateFormatter

COLUMN_ORDER = [
    "teamNumber",
    "entries",
    "avgAutoFuel",
    "avgTransitionFuel",
    "avgFirstActiveHubFuel",
    "avgSecondActiveHubFuel",
    "avgTeleopFuel",
    "avgEndgameFuel",
    "avgTotalFuel",
]

TEAMS = [
    "1000",
]


def avg(lst):
    return round(sum(lst) / len(lst), 2) if lst else 0


with open("fetched_data.json", "r") as f:
    fetched_data = json.load(f)
print(f"Loaded data for {len(fetched_data)} teams")
processedData = {
    "teamNumber": TEAMS,
    "entries": [],
    "avgAutoFuel": [],
    "avgTransitionFuel": [],
    "avgFirstActiveHubFuel": [],
    "avgSecondActiveHubFuel": [],
    "avgTeleopFuel": [],
    "avgEndgameFuel": [],
    "avgTotalFuel": [],
}
for team in TEAMS:
    team_matches = fetched_data.get(team, {})
    processedData["entries"].append(len(team_matches))
    autoFuels = []
    transitionFuels = []
    firstActiveHubFuels = []
    secondActiveHubFuels = []
    teleopFuels = []
    endgameFuels = []
    totalFuels = []
    for match_id, match_data in team_matches.items():

        def get_value(field):
            if isinstance(field, dict):
                if "integerValue" in field:
                    return int(field["integerValue"])
                elif "doubleValue" in field:
                    return float(field["doubleValue"])
                elif "booleanValue" in field:
                    return field["booleanValue"]
            return 0

        autoFuel = get_value(match_data.get("autoFuel", {}))
        transitionFuel = get_value(match_data.get("transitionFuel", {}))
        firstActiveHubShift = 1 if get_value(match_data.get("shift1HubActive")) else 2
        secondActiveHubShift = 3 if get_value(match_data.get("shift3HubActive")) else 4
        endgameFuel = get_value(match_data.get("endgameFuel", {}))

        totalFuel = autoFuel + transitionFuel + endgameFuel + get_value(match_data.get(f"shift{firstActiveHubShift}Fuel", {})) + get_value(match_data.get(f"shift{secondActiveHubShift}Fuel", {}))
        autoFuels.append(autoFuel)
        transitionFuels.append(transitionFuel)
        firstActiveHubFuels.append(
            get_value(match_data.get(f"shift{firstActiveHubShift}Fuel"))
        )
        secondActiveHubFuels.append(
            get_value(match_data.get(f"shift{secondActiveHubShift}Fuel"))
        )
        endgameFuels.append(endgameFuel)
        totalFuels.append(totalFuel)
        
for id in range(TEAMS):
    
    
