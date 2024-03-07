import pathlib
from clean.clean_scrap import clean_scrap
from linkage.match import match

selected_npi = pathlib.Path(__file__).parent / "selected_columns.csv"
selected_scrap = pathlib.Path(__file__).parent / "selected_columns_s.csv"

#Because of size, not available at Git
scrap = 'local'
npi = 'local'
impact = 'local'

#Data used for visualization
clean_scrap(scrap, selected_scrap).to_csv(
    pathlib.Path(__file__).parent / "data/county_care.csv", index=False
)
match(npi, scrap, impact, selected_npi, selected_scrap).to_csv(
    pathlib.Path(__file__).parent / "data/merge.csv", index=False
)
