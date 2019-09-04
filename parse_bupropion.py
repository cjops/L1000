#!/usr/bin/env python
import pandas as pd
from cmapPy.pandasGEXpress.parse import parse
import cmapPy.pandasGEXpress.write_gct as wg
import cmapPy.pandasGEXpress.write_gctx as wgx
gctx_file =      "GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx" # 20 gigs
sig_info_file =  "GSE92742_Broad_LINCS_sig_info.txt"
gene_info_file = "GSE92742_Broad_LINCS_gene_info.txt"
pert_info_file = "GSE92742_Broad_LINCS_pert_info.txt"
cell_info_file = "GSE92742_Broad_LINCS_cell_info.txt"

# get metadata

# columns
sig_info = pd.read_csv(
    sig_info_file,
    sep="\t"
)
sig_info.set_index("sig_id", inplace=True)

# rows
gene_info = pd.read_csv(
    gene_info_file,
    sep="\t",
    dtype={'pr_gene_id': 'str'}
)
gene_info.set_index("pr_gene_id", inplace=True)

# norketamine
pert_ids = ["BRD-A05186015"]
sig_ids = sig_info[sig_info["pert_id"].isin(pert_ids) & sig_info["cell_id"].isin(["NPC", "NEU"])].index


# parse in GCTx
gctoo = parse(gctx_file, cid=sig_ids)

# set metadata
gctoo.col_metadata_df = sig_info.loc[sig_ids]
gctoo.row_metadata_df = gene_info

# write a GCT file
wg.write(gctoo, "bupropion")

del gctoo
