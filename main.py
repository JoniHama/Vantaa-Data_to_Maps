import geopandas as gpd
import pandas
import pandas as pd
import requests
from requests import Request
import re
from owslib.wfs import WebFeatureService
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
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


def exceldata(answer):
    print("Data", answer)
    populationdata = []
    if answer == "retirees" or answer == "eläkeläiset":
        if os.path.isfile("Vantaadata.xlsx"):
            df = pandas.read_excel("Vantaadata.xlsx", "1.3")
        else:
            url = "https://datastore.hri.fi/Vantaa/vaesto/Vantaan_vaesto_2020_2021.xlsx"
            myfile = requests.get(url, allow_redirects=True)
            open("Vantaadata.xlsx", "wb").write(myfile.content)
            df = pandas.read_excel("Vantaadata.xlsx", "1.3")
        datalocation = 10
        addition = 0
    elif answer == "migration" or answer == "muuttoliike":
        if os.path.isfile("Vantaadata.xlsx"):
            df = pandas.read_excel("Vantaadata.xlsx", "2.23")
        else:
            url = "https://datastore.hri.fi/Vantaa/vaesto/Vantaan_vaesto_2020_2021.xlsx"
            myfile = requests.get(url, allow_redirects=True)
            open("Vantaadata.xlsx", "wb").write(myfile.content)
            df = pandas.read_excel("Vantaadata.xlsx", "2.23")
        datalocation = 1
        addition = 1
        dfmigration = pandas.read_excel("Vantaadata.xlsx", "1.3")

    data = {
        "id": ["1"],
        "name": ["2"],
        "data": ["3"]
    }
    df2 = pd.DataFrame(data)

    for x in range(0, 11):
        n = df.iloc[8 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[8+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[8 + x, 1])
        df2.loc[x] = [str(a), b, c]

    for x in range(0, 10):
        n = df.iloc[20 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[20+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[20 + x, 1])
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 6):
        n = df.iloc[31 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[31+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[31 + x, 1])
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 10):
        n = df.iloc[38 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[38+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[38 + x, 1])
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 6):
        n = df.iloc[49 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[49+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[49 + x, 1])
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 9):
        n = df.iloc[56 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[56+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[56 + x, 1])
        df2.loc[len(df2.index)] = [str(a), b, c]

    for x in range(0, 9):
        n = df.iloc[66 + addition + x, 0]
        a = [int(s) for s in re.findall(r'\b\d+\b', n)]
        a = a[0]
        b = ''.join([i for i in n if not i.isdigit()]).strip()
        c = df.iloc[66+x + addition, datalocation]
        if answer == "migration" or answer == "muuttoliike":
            populationdata.append(dfmigration.iloc[66 + x, 1])
        df2.loc[len(df2.index)] = [str(a), b, c]

    if answer == "migration" or answer == "muuttoliike":
        for index, row in df2.iterrows():
            print("Populationdata", populationdata[index])
            print(row['data'])
            row['data'] = (row['data'] / populationdata[index]) * 100

            if populationdata[index] < 50:
                row['data'] = 0

    return df2
def mergedata(excel, ax):

    for index, row in ax.iterrows():
        a = row['kosanimi']
        b = excel.loc[excel['name'] == a]["data"].values
        if "data" not in ax:
            ax.insert(5, "data", b[0])
        ax.loc[index] = [row["id"], row['kosanimi'], row["kosa_ruotsiksi"], row["suuralue"], row["geometry"], b]

    return ax
def main():
    datasetsFIN = ["eläkeläiset", "muuttoliike"]
    datasetsEN = ["retirees", "migration"]
    language = ""
    answer = ""

    while language.casefold() != "en" and language.casefold() != "fin":
        language = input(f'Hello! What is your preferred language? (FIN/EN) ')

    if language.casefold() == "fin":
        for dataset in datasetsFIN:
            print(dataset)
        while answer not in datasetsFIN:
            answer = input("Minkä datan haluaisit käsiteltävän? ")
    else:
        for dataset in datasetsEN:
            print(dataset)
        while answer not in datasetsEN:
            answer = input("Which dataset would you like to process? ")

    ax = accessingdata()
    excel = exceldata(answer)
    ax = mergedata(excel, ax)

    ax = ax[ax.data != ".."]
    ax['data'] = ax['data'].astype("int64")
    fig, ao = plt.subplots(1, 1, figsize = (15,10))
    ao.set_axis_off();
    if answer == "retirees" or answer == "eläkeläiset":
        if language.casefold() == "fin":
            ao.set_title("Eläkeläisten osuus prosentteina Vantaan eri kaupunginosissa", fontsize=20)
            ax.plot(column='data', cmap="OrRd", ax=ao, legend=True, legend_kwds={'label': "Eläkeläiset prosentteina",
                                                                                    "orientation": "vertical"})
        else:
            ao.set_title("Percentage of retirees in the districts of Vantaa", fontsize=20)
            ax.plot(column='data', cmap="OrRd", ax=ao, legend=True, legend_kwds={'label': "Retirees in percentages",
                                                                                    "orientation": "vertical"})
    elif answer == "migration" or answer == "muuttoliike":
        vmin, vmax, vcenter = ax.data.min(), ax.data.max(), 0
        norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)

        if language.casefold() == "fin":
            ao.set_title("Väestönmuutokset suhteessa väkilukuun kaupunginosittain vuonna 2020", fontsize=20)
            ax.plot(column='data', cmap="coolwarm", ax=ao, legend=True, norm=norm, legend_kwds={'label': "Väestönmuutos prosentteina väkilukuun verrattuna",
                                                                                    "orientation": "vertical"})
        else:
            ao.set_title("Population change in the districts of Vantaa in percentages (2020)", fontsize=20)
            ax.plot(column='data', cmap="coolwarm", ax=ao, legend=True, norm=norm, legend_kwds={'label': "Change in percentage",
                                                                                    "orientation": "vertical"})
    ax['coords'] = ax['geometry'].apply(lambda x: x.representative_point().coords[:])
    ax['coords'] = [coords[0] for coords in ax['coords']]
    for idx, row in ax.iterrows():
        plt.annotate(text=row['kosanimi'], xy=row['coords'],
                     horizontalalignment='center', fontsize=10)
    plt.savefig("testi.png", dpi=199)
    plt.show()

if __name__ == '__main__':
    main()
