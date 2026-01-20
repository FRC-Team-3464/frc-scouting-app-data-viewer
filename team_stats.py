import json
from collections import defaultdict
from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, ColumnDataSource, DataTable, TableColumn
from bokeh.layouts import column
from bokeh.io import curdoc

# Load the fetched data
with open("fetched_data.json", "r") as f:
    data = json.load(f)


# Helper function to extract values from Firestore format
def get_value(obj):
    if isinstance(obj, dict):
        if "integerValue" in obj:
            return int(obj["integerValue"])
        elif "stringValue" in obj:
            return obj["stringValue"]
        elif "booleanValue" in obj:
            return obj["booleanValue"]
    return None


# Aggregate data by team number
team_stats = defaultdict(
    lambda: {
        "matches": [],
        "autoFuel": [],
        "firstActiveHubFuel": [],
        "secondActiveHubFuel": [],
    }
)

# Parse the nested JSON structure
for team_id, matches in data.items():
    for match_id, match_data in matches.items():
        team_num = get_value(match_data.get("teamNumber"))

        if team_num:
            team_num = str(team_num)
            team_stats[team_num]["matches"].append(
                get_value(match_data.get("matchNumber"))
            )
            team_stats[team_num]["autoFuel"].append(
                get_value(match_data.get("autoFuel", {})) or 0
            )

            # Find first and second active hub fuel
            shifts = [
                ("shift1HubActive", "shift1Fuel"),
                ("shift2HubActive", "shift2Fuel"),
                ("shift3HubActive", "shift3Fuel"),
                ("shift4HubActive", "shift4Fuel"),
            ]

            active_hub_fuels = []
            for hub_field, fuel_field in shifts:
                hub_active = get_value(match_data.get(hub_field))
                if hub_active:
                    fuel_value = get_value(match_data.get(fuel_field, {})) or 0
                    active_hub_fuels.append(fuel_value)

            # Add first and second active hub fuel (or 0 if not available)
            team_stats[team_num]["firstActiveHubFuel"].append(
                active_hub_fuels[0] if len(active_hub_fuels) > 0 else 0
            )
            team_stats[team_num]["secondActiveHubFuel"].append(
                active_hub_fuels[1] if len(active_hub_fuels) > 1 else 0
            )


# Prepare data for Bokeh table
table_data = {
    "Team Number": [],
    "Matches": [],
    "Avg Auto Fuel": [],
    "Avg First Active Hub Fuel": [],
    "Avg Second Active Hub Fuel": [],

}

for team_num in sorted(team_stats.keys(), key=lambda x: int(x) if x.isdigit() else 0):
    stats = team_stats[team_num]
    num_matches = len(stats["matches"])

    table_data["Team Number"].append(team_num)
    table_data["Matches"].append(num_matches)
    table_data["Avg Auto Fuel"].append(
        round(sum(stats["autoFuel"]) / num_matches if num_matches > 0 else 0, 2)
    )
    table_data["Avg First Active Hub Fuel"].append(
        round(
            sum(stats["firstActiveHubFuel"]) / num_matches if num_matches > 0 else 0, 2
        )
    )
    table_data["Avg Second Active Hub Fuel"].append(
        round(
            sum(stats["secondActiveHubFuel"]) / num_matches if num_matches > 0 else 0, 2
        )
    )


# Create Bokeh data table
source = ColumnDataSource(table_data)

columns = [
    TableColumn(field="Team Number", title="Team Number", width=100),
    TableColumn(field="Matches", title="Matches", width=80),
    TableColumn(field="Avg Auto Fuel", title="Avg Auto Fuel", width=130),
    TableColumn(
        field="Avg First Active Hub Fuel", title="Avg First Active Hub Fuel", width=180
    ),
    TableColumn(
        field="Avg Second Active Hub Fuel",
        title="Avg Second Active Hub Fuel",
        width=180,
    ),
    TableColumn(field="Auto Climbed", title="Auto Climbed", width=120),
    TableColumn(field="Under Trench", title="Under Trench", width=120),
    TableColumn(field="Auto Bump", title="Auto Bump", width=110),
    TableColumn(field="Played Defense", title="Played Defense", width=130),
]

data_table = DataTable(source=source, columns=columns, width=1400, height=400)

# Create bar chart for avg fuel by team
p = figure(
    x_range=table_data["Team Number"],
    title="Average Auto Fuel by Team",
    toolbar_location="right",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

p.vbar(
    x="Team Number",
    top="Avg Auto Fuel",
    width=0.8,
    source=source,
    fill_color="navy",
    line_color="white",
)

p.xaxis.axis_label = "Team Number"
p.yaxis.axis_label = "Average Fuel"
p.add_tools(
    HoverTool(tooltips=[("Team", "@{Team Number}"), ("Avg Fuel", "@{Avg Auto Fuel}")])
)

# Output to HTML
output_file("team_stats.html")
layout = column(data_table, p)
save(layout)

print("Bokeh visualization saved to team_stats.html")
