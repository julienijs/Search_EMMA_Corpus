import os
import re
import codecs
from tqdm import tqdm

import pandas
from bs4 import BeautifulSoup

# Define the location of the directory
directory = r"C:/Users/u0149275/OneDrive - KU Leuven/keep_Ving/emma-1.0_full/EMMA_Corpus/corpus/test"

# Change the directory
os.chdir(directory)


# Reading the data inside the xml file to a variable under the name data
def read_file(path):
    with codecs.open(path, encoding='utf-8', mode='r') as f:
        data = f.read()
        bs_data = BeautifulSoup(data, 'xml')  # Passing the stored data inside the beautifulsoup parser
        texts = bs_data.find_all('doc')  # Finding all instances of tag
        hits_df = pandas.DataFrame(columns=column_names)
        for text in texts:
            pattern = r"kee?ps?t??[a-zA-Z0-9_\n ]*\w+ing[\W]*"  # regex: looks for keep + -ing form
            for match in re.finditer(pattern, str(text)):
                lcontext = str(text)[match.start()-100: match.start()]
                kwic = str(text)[match.start(): match.end()]
                rcontext = str(text)[match.end(): match.end()+100]
                filename = os.path.basename(path)
                hits_df.loc[len(hits_df)] = [str(filename), str(lcontext), str(kwic), str(rcontext)]
        return hits_df


column_names = ["File", "Left_Context", "Hit", "Right_Context"]
final_df = pandas.DataFrame(columns=column_names)

# Iterate over all the files in the directory
for file in tqdm(os.listdir(), total=13750):
    try:
        if file.endswith('.xml'):
            file_path = f"{directory}/{file}"  # Create the filepath of particular file
            out_df = read_file(file_path)
            final_df = pandas.concat([final_df, out_df])
    except:
        print(file)

# add metadata
metadata = pandas.read_excel("C:/Users/u0149275/OneDrive - KU "
                             "Leuven/keep_Ving/emma-1.0_full/EMMA_Corpus/EMMA_metadata_copy.xlsx",
                             sheet_name=0, header=0)
print(metadata)
final_df = final_df.merge(metadata, how='inner', left_on='File', right_on='Clean_FileName')
print(final_df)
final_df.to_excel("output.xlsx")
