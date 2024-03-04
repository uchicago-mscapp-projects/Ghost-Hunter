import pathlib
from clean.clean_scrap import clean_scrap
from linkage.match import match

selected_npi = pathlib.Path(__file__).parent / "selected_columns.csv"
selected_scrap = pathlib.Path(__file__).parent / "selected_columns_s.csv"
scrap = pathlib.Path(__file__).parent / "ccare_results_clean.json"
npi = "https://drive.google.com/file/d/1XoFuh9wP999pa4kcbb-lCCTXJBqYzBBv/view?usp=share_link"
impact = "https://drive.google.com/file/d/1GFP_fN-o-xVTBpv1EOZrKGqTf45KDKu3/view?usp=share_link"

clean_scrap(scrap, selected_scrap).to_csv(
    pathlib.Path(__file__).parent / "data/county_care.csv", index=False
)
match(npi, scrap, impact, selected_npi, selected_scrap).to_csv(
    pathlib.Path(__file__).parent / "data/merge.csv", index=False
)
