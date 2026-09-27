import json, sys
from openpyxl import load_workbook
f = sys.argv[1] if len(sys.argv) > 1 else "out/D7_Integrated_Model.xlsx"
wb = load_workbook(f, data_only=True); m = json.load(open("out/rowmap.json"))
def row(ws, r, cols="BCDEFGHIJKLMNOPQ"):
    w = wb[ws]; return [w[f"{c}{r}"].value for c in cols]
fmt = lambda v: (f"{v:8.2f}" if isinstance(v, (int, float)) else f"{str(v)[:8]:>8}")
def show(ws, key, mp, lab=None):
    print(f"{(lab or key)[:26]:26}", " ".join(fmt(x) for x in row(ws, mp[key])))
print(" " * 26, "   FY26 ", "  ".join(["Q1-27", "Q2", "Q3", "Q4", "Q1-28", "Q2", "Q3", "Q4", "Q1-29", "Q2", "Q3", "Q4", "FY27", "FY28", "FY29"]))
for k in ["hc", "rea", "eff"]: show("Capacity", k, m["CAP"])
for k in ["win", "cyc", "deal", "cap", "sup", "work", "dir", "pipe"]: show("Bookings", k, m["br"])
for k in ["open", "dir", "par", "expn", "cont", "chrn", "vaj", "close"]: show("ARR_bridge", k, m["ab"])
for k in ["nl", "growth", "gapb", "nrr", "inc"]: show("ARR_bridge", k, m["ann"])
for k in ["rev", "gmpost", "sm", "ebitda", "cac", "smarr"]: show("PnL", k, m["pl"])
w = wb["Channel"]
for k in ["parr", "share", "pm", "net", "be", "preq", "pcap"]: print(f"{k:26}", [round(w[f'{c}{m["hc"][k]}'].value, 3) for c in "OPQ"])
w = wb["Investment"]
for k in ["ae", "ch", "tot", "env", "head", "pbk"]: print(f"inv {k:22}", [w[f'{c}{m["ir"][k]}'].value for c in "JKL"])
w = wb["Bookings"]
for k in m["bp"]: print(f"bp {k:23}", [round(w[f'{c}{m["bp"][k]}'].value, 3) for c in "OPQ"])
w = wb["Checks"]
for r in range(5, 30):
    if w[f"A{r}"].value: print(f"{w[f'A{r}'].value[:62]:62}", w[f"B{r}"].value, w[f"C{r}"].value)
w = wb["Inject4"]; print("inj4", [w[f"C{r}"].value for r in (12, 13, 15, 16)])
