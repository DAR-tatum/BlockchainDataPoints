import pandas as pd
import os
import argparse
    

def handle_file(dirpath, filename):
    filepath = os.path.join(dirpath, filename)
    
    if filename.endswith('.csv'):
        try:
            return pd.read_csv(filepath, delim_whitespace=True)
        except pd.errors.EmptyDataError:
            print(f'Skipping empty file {filepath}')   
    return
    
    
parser = argparse.ArgumentParser()
parser.add_argument('--outdir', type=str, help='Output directory path', required=True)
args = parser.parse_args()
outdir = args.outdir
    
data = {}

for dirpath, dirnames, filenames in os.walk('./'):
    for filename in filenames:
        df = handle_file(dirpath, filename)
        if df is not None:
            dir = dirpath.split('/')[-2]
            token = dirpath.split('/')[-1]

            if dir not in data:
                if 'date' not in df.columns:
                    data[token + '_' + dir] = df
                else:
                    df.columns = ['date'] + [token + '_' + col for col in df.columns[1:]]
                    data[dir] = df
            else:
                df.columns = ['date'] + [token + '_' + col for col in df.columns[1:]]
                data[dir] = pd.merge(data[dir], df, on='date', how='outer')


with pd.ExcelWriter(outdir, engine='xlsxwriter') as writer:
    for dir, df in data.items():
        sheet_name = dir.replace('/', '_')
        
        if len(sheet_name) > 30:
            sheet_name = sheet_name[:30]
            
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # adjusts the columns to fit content
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)
                
    #writer.save()
