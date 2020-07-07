import pandas as pd
import folium

#Create a map in the background and save it

m = folium.Map(location=[48.85, 2.35], tiles="OpenStreetMap", zoom_start=2.5, min_zoom=2.5)
m.save("mymap.html")

#Access the covid dataset and clean data by removing unneccesary columns

covid = pd.read_csv("country_wise_latest.csv")
covid.drop(['Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered', 'Deaths / 100 Cases', 'Recovered / 100 Cases', 'Deaths / 100 Recovered',
         'Confirmed last week', '1 week change', '1 week % increase', 'WHO Region'], axis=1, inplace=True)

#Access a dataset containing countries and their coordinates and drop initials

countries = pd.read_csv("countries.csv")
countries.drop(["country"], axis = 1, inplace = True)


#rename columns and then merge datasets to contain country name, cases confirmed, and coordinates

covid.columns = ['name', "Confirmed"]
covid.at[173,'name'] = 'United States'
countries = countries.merge(covid, on = "name", how = "left")
countries["Confirmed"].fillna(0, inplace = True)
countries["longitude"].fillna(0, inplace = True)
countries["latitude"].fillna(0, inplace = True)


# Add markers onto the map

for i in range(0, len(countries)):
    folium.Circle(
        location=[countries.iloc[i]['latitude'], countries.iloc[i]['longitude']],
        popup= ("Country: " + str(countries.iloc[i]['name']) + "\nCases Cofirmed: " + str(countries.iloc[i]['Confirmed']) ),
        radius=countries.iloc[i]['Confirmed'] / 2.0,
        color='navy',
        fill=True,
        fill_color='navy'
    ).add_to(m)

# Save it as html
m.save('mymap.html')



