import geopandas as gpd
import pandas
import pandas as pd
import requests
from requests import Request
import re
from owslib.wfs import WebFeatureService
import matplotlib.pyplot as plt
import os

def accessingdata():
    url = "https://gis.vantaa.fi/geoserver/wfs"
    wfs = WebFeatureService(url=url)
    layer = list(wfs.contents)[3]
    print(layer)

    params = dict(service='WFS', version="1.0.0", request='GetFeature',
                  typeName=layer, outputFormat='json')
    q = Request('GET', url, params=params).prepare().url
    data = gpd.read_file(q)
    return data


def exceldata(): # row 8 for names; column 10 for 65+
    if os.path.isfile("Vantaadata.xlsx"):
        df = pandas.read_excel("Vantaadata.xlsx", "1.3")
    else:
        url = "https://datastore.hri.fi/Vantaa/vaesto/Vantaan_vaesto_2020_2021.xlsx"
        myfile = requests.get(url, allow_redirects=True)
        open("Vantaadata.xlsx", "wb").write(myfile.content)
        df = pandas.read_excel("Vantaadata.xlsx", "1.3")

    data = {
        "id": ["1"],
        "name": ["2"],
        "percent": ["3"]
    }
    df2 = pd.DataFrame(data)

    for x in range(0, 11):
        n = df.iloc[8 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[8+x,10]
        df2.loc[x] = [str(a), b, c]

    for x in range(0, 10):
        n = df.iloc[20 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[20+x, 10]
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 6):
        n = df.iloc[31 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[31+x, 10]
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 10):
        n = df.iloc[38 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[38+x, 10]
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 6):
        n = df.iloc[49 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[49+x, 10]
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 9):
        n = df.iloc[56 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[56+x, 10]
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 9):
        n = df.iloc[66 + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[66+x, 10]
        df2.loc[len(df2.index)] = [str(a), b, c]


    return df2
def mergedata(excel, ax):

    for index, row in ax.iterrows():
        a = row['kosanimi']
        b = excel.loc[excel['name'] == a]["percent"].values
        if "percent" not in ax:
            ax.insert(5, "percent", b[0])
        ax.loc[index] = [row["id"], row['kosanimi'], row["kosa_ruotsiksi"], row["suuralue"], row["geometry"], b]

    return ax
def main():
    ax = accessingdata()
    excel = exceldata()
    ax = mergedata(excel, ax)

    ax = ax[ax.percent != ".."]
    ax['percent'] = ax['percent'].astype("int64")
    fig, ao = plt.subplots(1, 1, figsize = (15,10))
    ao.set_axis_off();
    ax.plot(column='percent', cmap="OrRd", ax=ao, legend=True, legend_kwds={'label': "Eläkeläiset prosentteina",
                                                               "orientation": "vertical"})

    ao.set_title("Eläkeläisten osuus prosentteina Vantaan eri kaupunginosissa", fontsize=20)
    ax['coords'] = ax['geometry'].apply(lambda x: x.representative_point().coords[:])
    ax['coords'] = [coords[0] for coords in ax['coords']]
    for idx, row in ax.iterrows():
        plt.annotate(text=row['kosanimi'], xy=row['coords'],
                     horizontalalignment='center', fontsize=10)
    plt.savefig("testi.png", dpi=199)
    plt.show()

if __name__ == '__main__':
    main()
