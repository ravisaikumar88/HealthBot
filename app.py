import streamlit as st
import requests
#using the concept of decision-tree

 
def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {
        'User-Agent': 'MyHospitalFinderApp/1.0 (myemail@example.com)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            st.error("City not found.")
            return None
    else:
        st.error(f"Error: {response.status_code} {response.text}")
        return None
 
def find_hospitals(city_name, radius=5000, max_results=5, name_filter=None):
    coordinates = get_coordinates(city_name)
    if coordinates:
        lat, lon = coordinates
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        node
          ["amenity"="hospital"]
          (around:{radius},{lat},{lon});
        out body;
        """
        headers = {
            'User-Agent': 'psarav/1.0 (akhilreddy6831@gmail.com)'
        }
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers)
        if response.status_code == 200:
            hospitals = response.json().get('elements', [])
            filtered_hospitals = []
            for hospital in hospitals:
                name = hospital.get('tags', {}).get('name', 'N/A')
                if name_filter and name_filter.lower() not in name.lower():
                    continue
                filtered_hospitals.append(hospital)
                if len(filtered_hospitals) >= max_results:
                    break
            return filtered_hospitals
        else:
            st.error(f"Error: {response.status_code} {response.text}")
            return []
    else:
        return []
 
st.title("Hospital Finder")
city_name = st.text_input("Enter the city name:")
name_filter = st.text_input("Enter a name filter (optional):")
 
if st.button("Find Hospitals"):
    hospitals = find_hospitals(city_name, name_filter=name_filter)
    if hospitals:
        st.write(f"Found {len(hospitals)} hospitals:")
        for hospital in hospitals:
            name = hospital.get('tags', {}).get('name', 'N/A')
            lat = hospital['lat']
            lon = hospital['lon']
            st.write(f"Name: {name}, Lat: {lat}, Lon: {lon}")
    else:
        st.write("No hospitals found.")

