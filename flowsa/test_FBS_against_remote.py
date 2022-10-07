"""
Tests to run during github action
"""
import sys

import pytest
import os
from flowsa import seeAvailableFlowByModels
from flowsa.metadata import set_fb_meta
from flowsa.settings import paths, diffpath
from flowsa.validation import compare_FBS_results
from flowsa.common import check_method_status
from esupy.processed_data_mgmt import download_from_remote


@pytest.mark.skip(reason="Perform targeted test for compare_FBS on PR")
def test_FBS_against_remote(only_run_m=None):
    """Compare results for each FBS method at current HEAD with most
    recent FBS stored on remote server."""
    outdir = diffpath
    method_status = check_method_status()
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for m in seeAvailableFlowByModels("FBS", print_method=False):
        if only_run_m is not None and m != only_run_m:
            continue
        status = download_from_remote(set_fb_meta(m, "FlowBySector"),
                                      paths)
        if not status:
            print(f"{m} not found in remote server. Skipping...")
            continue
        if method_status.get(m) is not None:
            print(f"{m} skipped due to "
                  f"{method_status.get(m).get('Status', 'Unknown')}")
            continue
        print("--------------------------------\n"
              f"Method: {m}\n"
              "--------------------------------")
        df = compare_FBS_results(m, m, compare_to_remote=True)
        df.rename(columns = {'FlowAmount_fbs1': 'FlowAmount_remote',
                             'FlowAmount_fbs2': 'FlowAmount_HEAD'},
                  inplace=True)
        if len(df) > 0:
            print(f"Saving differences in {m} to csv")
            df.to_csv(f"{outdir}{m}_diff.csv", index=False)
        else:
            print(f"***No differences found in {m}***")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_FBS_against_remote()
    elif sys.argv[1] == "list":
        print("\n".join(seeAvailableFlowByModels("FBS", print_method=False)))
    else:
        test_FBS_against_remote(sys.argv[1])
