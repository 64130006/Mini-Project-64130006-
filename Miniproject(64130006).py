import pandas as pd
from math import radians, cos, sin, asin, sqrt


def cleandata(df):

    df = df.drop(columns=['velocity', 'heading', 'vertrate', 'callsign', 'alert', 'spi', 'squawk', 'geoaltitude',
                          'lastposupdate', 'lastcontact', 'hour'])
    df = df.sort_values(['time'])
    df = df[df.onground == False]
    df = df.drop(columns=['onground'])
    df = df.reset_index(drop=True)

    return df


def checkhorizon(lat1, lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))
    r = 3437.67
    distance = c * r
    # print(distance)
    return distance < 3


def main():

    pd.set_option('display.max_columns', None)

    dataframe = pd.read_csv(r'C:\Users\IAAI-COM-SSD\PycharmProjects\pythonProject\day4.csv')
    #print(dataframe.head(50))
    dataframe = cleandata(dataframe)
    #print(dataframe.head(50))

    # dataframe = dataframe.head(100)

    index = dataframe.index
    Vcount = 0
    Hcount = 0
    for i in index:
        j = i + 1
        if j not in index:
            break
        while dataframe.at[i, 'time'] == dataframe.at[j, 'time']:
            if abs(dataframe.at[i, 'baroaltitude'] - dataframe.at[j, 'baroaltitude']) < 304.8:
                Vcount += 1
                print('V', Vcount, i, j)
            if checkhorizon(dataframe.at[i, 'lat'], dataframe.at[i, 'lon'],
                            dataframe.at[j, 'lat'], dataframe.at[j, 'lon']):
                Hcount += 1
                print('H', Hcount, i, j)
            j += 1
            if j not in index:
                break
    print("_______________________")
    print(Vcount)
    print(Hcount)




if __name__ == '__main__':
    main()