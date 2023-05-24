import pandas as pd
import geopy.geocoders

# Read raw csv data
df=pd.read_csv('./dataset/college-salaries/salaries-by-region.csv')

# Initialize geolocator
geolocator = geopy.geocoders.Nominatim(user_agent="college_salaries_visualization")
df['lat'] = None
df['lon']=None

# Search for location
for index, row in df.iterrows():
    location = geolocator.geocode(row['School Name'])
    if location is not None:
        df.at[index, 'lat'] = location.latitude
        df.at[index, 'lon'] = location.longitude

# Save to csv
print(df)
df.to_csv('./dataset/processed/salaries-by-region-geocoded.csv', index=False)
