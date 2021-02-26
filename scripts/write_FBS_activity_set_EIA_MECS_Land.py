# write_FBS_activity_set_BLM_PLS.py (scripts)
# !/usr/bin/env python3
# coding=utf-8


"""
Write the csv called on in flowbysectormethods yaml files for land use related to EIA MECS
"""

import flowsa
from flowsa.common import flowbysectoractivitysetspath


if __name__ == '__main__':

    # define mecs land fba parameters
    land_flowclass = 'Land'
    land_years = [2010, 2014]
    datasource = 'EIA_MECS_Land'

    # Read BLM PLS crosswalk
    df_import = flowsa.getFlowByActivity(datasource, land_years, land_flowclass)

    # drop unused columns
    df = df_import[['ActivityConsumedBy']].drop_duplicates()
    df = df[~df['ActivityConsumedBy'].str.contains('-')]

    # rename columns
    df = df.rename(columns={"ActivityConsumedBy": "name"})

    # assign column values
    df = df.assign(activity_set='activity_set_1')
    df = df.assign(note='')

    # reorder dataframe
    df = df[['activity_set', 'name', 'note']]
    df = df.sort_values(['activity_set', 'name']).reset_index(drop=True)

    # save df
    df.to_csv(flowbysectoractivitysetspath + datasource + "_asets.csv", index=False)
