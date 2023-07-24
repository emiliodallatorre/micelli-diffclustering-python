from pandas import DataFrame, read_excel, read_pickle
from os import path
from numpy import int64

from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

base_path: str = "data/"

data: DataFrame

if not path.isfile(f"{base_path}data.pkl"):
    data = read_excel(f"{base_path}project.xlsx")
    data.to_csv(f"{base_path}data.csv")
    data.to_pickle(f"{base_path}data.pkl")
data = read_pickle(f"{base_path}data.pkl")
data = data.infer_objects()

# We need to cast strs to floats, as some of them are misrepresented
columns_with_floats_as_strs: list[str] = ["totalCost", "ecMaxContribution"]
for column_with_floats_as_strs in columns_with_floats_as_strs:
  data[column_with_floats_as_strs] = data[column_with_floats_as_strs].str.replace(",", ".").astype("float")

# We need to convert dates to their epoch representation
columns_with_datetimes: list[str] = ["startDate", "endDate", "ecSignatureDate"]
for column_with_datetimes in columns_with_datetimes:
  data[column_with_datetimes] = data[column_with_datetimes].values.astype(int64) // 10 ** 9

# ====================
useless_columns: list[str] = ["id", "acronym", "status", "title", "nature", "objective", "contentUpdateDate", "rcn", "grantDoi"]

meaningful_data: DataFrame = data.drop(useless_columns, axis=1)
meaningful_data.info()
