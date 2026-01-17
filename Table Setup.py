
from bokeh.io import show
from bokeh.models import ColumnDataSource,DataTable,TableColumn
import random

data = dict(
    phases= ["auto", "transition","phase1","phase2","phase3","phase4","endgame"],
    scores = [random.randint(0,100) for i in range(7)]
)
source = ColumnDataSource(data)

columns =[
    TableColumn(field = "phases", title = "Phases"),
    TableColumn(field = "scores", title="Scores")
]
data_table = DataTable(source=source, columns=columns, width =800, height=400)
show(data_table)