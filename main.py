from enum import Enum,IntEnum
from typing import Optional
import pandas as pd
from pathlib import Path
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--folder", type=Path, help='Carpetas donde se encuentran los csv')
parser.add_argument("--dest", type=Path, help='destino donde se va a dejar el csv')
parser.add_argument("--threshold", type=float, help='Ratio de vacios permitidos', required=False)
args = parser.parse_args()

folder = Path(args.folder)
if not folder.exists() or not folder.is_dir():
   print('Ingresa bien la ruta')
   exit()

dest = Path(args.dest)
if dest.suffix != '.csv':
   print('La ruta destino debe de ser un csv')
   exit()

threshold= float(args.threshold) or 0.2

if threshold <0 or threshold >1:
   print('Revisa el threshold')
   exit()

csv_files = folder.glob('*.csv')
df = None
for f in csv_files:
   df_aux = pd.read_csv(f,
   )
   if df is None:
      df = df_aux
      continue
   df = pd.concat([df,df_aux])
mask = (df.notna().sum() / len(df)) >= threshold

cols_to_keep = df.columns[mask].tolist()
df = df[cols_to_keep]
df.to_csv(dest, sep=';',encoding='utf-8', index = False)
