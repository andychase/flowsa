# USGS_MYB_Nickel.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8

import io
from flowsa.flowbyfunctions import assign_fips_location_system
from flowsa.data_source_scripts.USGS_MYB_Common import *

"""

Projects
/
FLOWSA
/

FLOWSA-314

Import USGS Mineral Yearbook data

Description

Table T1 and T10

SourceName: USGS_MYB_Nickel
https://www.usgs.gov/centers/nmic/nickel-statistics-and-information

Minerals Yearbook, xls file, tab T10 and T1:
Data for: Nickel; mine

Years = 2012+
"""
SPAN_YEARS = "2012-2016"

def usgs_nickel_url_helper(build_url, config, args):
    """Used to substitute in components of usgs urls"""
    url = build_url
    return [url]


def usgs_nickel_call(url, usgs_response, args):
    """Calls the excel sheet for nickel and removes extra columns"""
    df_raw_data = pd.io.excel.read_excel(io.BytesIO(usgs_response.content), sheet_name='T10')# .dropna()
    df_data_1 = pd.DataFrame(df_raw_data.loc[36:36]).reindex()
    df_data_1 = df_data_1.reset_index()
    del df_data_1["index"]

    df_raw_data_two = pd.io.excel.read_excel(io.BytesIO(usgs_response.content), sheet_name='T1')  # .dropna()
    df_data_2 = pd.DataFrame(df_raw_data_two.loc[11:16]).reindex()
    df_data_2 = df_data_2.reset_index()
    del df_data_2["index"]

    if len(df_data_1.columns) > 11:
        for x in range(11, len(df_data_1.columns)):
            col_name = "Unnamed: " + str(x)
            del df_data_1[col_name]

    if len(df_data_1. columns) == 11:
        df_data_1.columns = ["Production", "space_1", "year_1", "space_2", "year_2", "space_3",
                             "year_3", "space_4", "year_4", "space_5", "year_5"]

    if len(df_data_2.columns) == 12:
        df_data_2.columns = ["Production", "space_1", "space_2", "year_1", "space_3", "year_2", "space_4",
                             "year_3", "space_5", "year_4", "space_6", "year_5"]

    col_to_use = ["Production"]
    col_to_use.append(usgs_myb_year(SPAN_YEARS, args["year"]))
    for col in df_data_1.columns:
        if col not in col_to_use:
            del df_data_1[col]
    for col in df_data_2.columns:
        if col not in col_to_use:
            del df_data_2[col]
    frames = [df_data_1, df_data_2]
    df_data = pd.concat(frames)
    df_data = df_data.reset_index()
    del df_data["index"]
    return df_data


def usgs_nickel_parse(dataframe_list, args):
    """Parsing the USGS data into flowbyactivity format."""
    data = {}
    row_to_use = ["Ores and concentrates3", "United States, sulfide ore, concentrate"]
    import_export = ["Exports:", "Imports for consumption:"]
    name = usgs_myb_name(args["source"])
    des = name
    dataframe = pd.DataFrame()
    for df in dataframe_list:
        prod = "production"
        for index, row in df.iterrows():
            if df.iloc[index]["Production"].strip() == "Exports:":
                prod = "exports"
            elif df.iloc[index]["Production"].strip() == "Imports for consumption:":
                prod = "imports"
            if df.iloc[index]["Production"].strip() in row_to_use:
                remove_digits = str.maketrans('', '', digits)
                product = df.iloc[index]["Production"].strip().translate(remove_digits)
                data = usgs_myb_static_varaibles()
                data["SourceName"] = args["source"]
                data["Year"] = str(args["year"])
                data["Unit"] = "Metric Tons"
                col_name = usgs_myb_year(SPAN_YEARS, args["year"])
                if product.strip() == "United States, sulfide ore, concentrate":
                    data["Description"] = "United States, sulfide ore, concentrate Nickel"
                    data["ActivityProducedBy"] = name
                    data['FlowName'] = name + " " + prod
                elif product.strip() == "Ores and concentrates":
                    data["Description"] = "Ores and concentrates Nickel"
                    data["ActivityProducedBy"] = name
                    data['FlowName'] = name + " " + prod
                if str(df.iloc[index][col_name]) == "--" or str(df.iloc[index][col_name]) == "(4)":
                    data["FlowAmount"] = str(0)
                else:
                    data["FlowAmount"] = str(df.iloc[index][col_name])
                dataframe = dataframe.append(data, ignore_index=True)
                dataframe = assign_fips_location_system(dataframe, str(args["year"]))
    return dataframe
