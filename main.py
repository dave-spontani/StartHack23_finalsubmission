import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import requests
from PIL import Image
import streamlit as st
from streamlit.elements.image import image_to_url, MAXIMUM_CONTENT_WIDTH
from PIL import Image
import pandas as pd
#import plotly.express as px
import plotly.graph_objects as go
import boto3
import time
from botocore.exceptions import NoCredentialsError
import mimetypes
import random
from math import sin, cos, sqrt, atan2, radians

def load_data():
    data = pd.read_csv('sammelstellen.csv', sep= ";")
    return data

sammelstellen = load_data()
sammelstellen[['latitude','longitude']] = sammelstellen['Geo Point'].str.split(',',expand=True)
x = sammelstellen.abfallarten.str.split(',', expand=True).stack()
sammelstellen[["Alttextilien",	"Altöl",	"Aluminium",	"Dosen",	"Glas",	"Sonderabfall",	"Styropor"]] =  pd.crosstab(x.index.get_level_values(0), x.values).iloc[:, 1:]

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0 # approximate radius of the Earth in km
    #print(lat2)
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(float(lat2))
    lon2_rad = radians(float(lon2))

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
#find closest point to location 
def find_closest_point(location, points):
    closest_point = None
    closest_distance = float('inf')
    
    for point in points:
        lat = points[point][0]
        lon = points[point][1]
        
        distance = calculate_distance(location['coords']['latitude'], location['coords']['longitude'], lat, lon)
        
        if distance < closest_distance:
            closest_distance = distance
            closest_point = point

    return closest_point


def generate_recycling_locations2(sammelstellen, location, required_recycling_types):
    latitudes = []
    longitudes = []
    names = []
    abfall = []

    # only using ONE recylcing type, filter out the sammelstellen that do not offer this type
    filtered_sammelstellen = sammelstellen[sammelstellen['abfallarten'].str.contains(required_recycling_types)]
    #print(filtered_sammelstellen)

    # create a dictionary with the location name as key and the coordinates as value
    cor_dict = dict(zip(filtered_sammelstellen["Standort"], zip(filtered_sammelstellen["latitude"], filtered_sammelstellen["longitude"])))    
    #print(cor_dict)
    
    # find the closest location to the user
    close_location = find_closest_point(location, cor_dict) #this is for some reason printing a shit ton
    #print("Closest location")
    #print(close_location)

    # get the index of the closest location
    location_index = sammelstellen.index[sammelstellen["Standort"] == close_location].tolist()

    #print("location index: " + str(location_index))

    lats = sammelstellen["latitude"][location_index].tolist()
    longs = sammelstellen["longitude"][location_index].tolist()
    #print(longs)
    noms =["You", close_location]
    #print(noms)
    
    return lats, longs, noms, required_recycling_types


# st.title("Wilkommen bei der Sperrgutentsorgung St. Gallen")

# location = get_geolocation()
# print(location)
# latitudes = []
# longitudes = []
# names = []

# for i in range(0, len(samstelstellen)):
#     newStrings = samstelstellen["Geo Point"][i].split(",")
    
#     latitudes.append(newStrings[0])
#     longitudes.append(newStrings[1])
#     names.append(samstelstellen["Standort"][i])



# if not location:

#     st.header("Bitte geben Sie uns folgende Angaben:")
#     strasse = st.text_input("Strasse")
#     nummer = st.text_input("Nummer")
#     plz = st.text_input("Postleitzahl")

#     location_input = strasse + nummer + plz 
#st.header("Ihre Adresse lautet: {}".format(location))

tab1, tab2, tab3= st.tabs(["Trash collector", "Recycling near you", "Too good to Throw"])

with tab1:
    

    def upload_file(remote_url, bucket, file_name):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        try:
            imageResponse = requests.get(remote_url, stream=True).raw
            content_type = imageResponse.headers['content-type']
            extension = mimetypes.guess_extension(content_type)
            s3.upload_fileobj(imageResponse, bucket, file_name + extension)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
    
    trans_dict = {"metal": "Altmetall", "glass": "Glas"}

    input_dict = {}
    
    lat_list =[47.4335382954281, 47.41847764687886, 47.422942, 47.434731, 47.437095]
    lon_list =[9.383928186686626, 9.36442953556214, 9.371181, 9.378949, 9.387298]
    usability= [1,1,0,1,0]
    marks = [1,2,2,1,1]
    urls = ["https://streamlitbuckethack23.s3.eu-central-1.amazonaws.com/apypydyzxd.jpg", "https://streamlitbuckethack23.s3.eu-central-1.amazonaws.com/abqab.jpg", "https://streamlitbuckethack23.s3.eu-central-1.amazonaws.com/pczyd.jpg", "https://streamlitbuckethack23.s3.eu-central-1.amazonaws.com/rpypb.jpg", "https://streamlitbuckethack23.s3.eu-central-1.amazonaws.com/xzcxp.jpg"]

    input_dict["latitute"] = lat_list
    input_dict["longitude"] = lon_list
    input_dict["usabiluty"] = usability
    input_dict["marks_needed"] = marks
    input_dict["urls"] = urls

    input_df = pd.DataFrame.from_dict(input_dict)

    st.title("Wilkommen bei der Sperrgutentsorgung St. Gallen")

    # location = get_geolocation()

    # if not location:

    #     st.header("Bitte geben Sie uns folgende Angaben:")
    #     strasse = st.text_input("Strasse")
    #     nummer = st.text_input("Nummer")
    #     plz = st.text_input("Postleitzahl")

    #     location_input = strasse + nummer + plz 

    # else:
    #     st.header("Ihr Standort wurde erfolgreich angenommen!")

    st.header("Laden Sie Bitte ein Foto des Sperrguts hoch:")
    picture = st.camera_input("Foto")
    kill_materials = ["metal", "glass","ceramic"]
    not_retriev = "N/A"
    furniture_types =  ["chair", "bed", "couch", "table", "matress","lamp", "sofa"]

    if picture:
        full_url = "placeholder"
        test = Image.open(picture)
        width, height = test.size  # width is needed for image_to_url()
        if width > MAXIMUM_CONTENT_WIDTH:
            width = MAXIMUM_CONTENT_WIDTH  # width is capped at 2*730 https://github.com/streamlit/streamlit/blob/949d97f37bde0948b57a0f4cab7644b61166f98d/lib/streamlit/elements/image.py#L39

        part_url = image_to_url(
                    image=picture,
                    width=width,
                    clamp=False,
                    channels="RGB",
                    output_format=picture.type,
                    image_id=picture.id,)  # each uploaded file has a file.id)

        leading_url = "https://dave-spontani-start-hack-23-test-file-nk8fhe.streamlit.app/~/+/"

        full_url = str(leading_url) + str(part_url)
        
        ACCESS_KEY_ID = "removed"
        SECRET_ACCESS_KEY = "removed"

        name = ''.join((random.choice('abcdxyzpqr') for i in range(10)))

        uploaded = upload_file(full_url, 'streamlitbuckethack23', name)

        st.write("Bild hochgeladen!")
        time.sleep(3)

        api_key = 'removed'
        api_secret = 'removed'
        image_url = 'https://streamlitbuckethack23.s3.eu-central-1.amazonaws.com/{}.jpg'.format(name)

        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
            auth=(api_key, api_secret))

        #st.write(response.json())

        all_responses = [[round(i["confidence"]) ,i["tag"]["en"]] for i in response.json()["result"]["tags"]]


        all_tags_list = [i[1] for i in all_responses if i[0] > 25]

        for mat in kill_materials:
            if mat in all_tags_list:
                not_retriev = mat
        if not_retriev != "N/A":
            st.write("The Auto-Tagger has identified {}. Please find the next special disposal site close to you:".format(not_retriev))
            
        else: 
            for furn in furniture_types:
                count = 0
                if furn in all_tags_list:
                    st.write("It looks like your object is a {}".format(furn))
                    st.write("All good!")
                    count += 1


            if count < 1:
                st.write("Please try a different photo, or classify the object manually")
        
    st.write("We'll try to locate you")
    location = get_geolocation()
    if location:
        st.write("Found you!")
    #st.write('Location: ', location)
    if not location:
        st.write('Location not found')
        adress_input = st.text_input('Your adress:', '')
        #st.write('Your entered adress:', adress_input)



    st.header("Weitere Informationen:")

    resusable_input = st.checkbox('Mein Sperrgut ist in gutem Zustand')
    if resusable_input:
        resusable_input = 1

    material_content_input = st.multiselect(
        'Your object is primarily made out of ...',
        ['Wood', 'Glass', 'Metal', 'Plastic'])

    if material_content_input:
        #st.write(type(material_content_input))
        material_content_input = [i.lower() for i in material_content_input]

    for mat in kill_materials:
        if mat in material_content_input:
            not_retriev = mat

    if not_retriev != "N/A":
            st.write("Your object primarily is made of {}. Please find the next special disposal site close to you:".format(not_retriev))
            

        
        #st.write('You have chosen:', material_content_input)

    slider_weight_input = st.select_slider(
        'Weight',
        options=['< 10kg', '10kg - 30kg', '>30kg'])
        #st.write('Selected Weight', slider_weight_input)
    if slider_weight_input:
        if slider_weight_input == '>30kg':
            st.write("Your object is too heavy to be taken with us. Please find the next special disposal site close to you:")
            



    slider_size_input = st.select_slider(
        'Size',
        options=['Small', 'Medium', 'Large'])
        #st.write('Selected Size', slider_size_input)
    if slider_size_input:
        if slider_size_input == "Large":
            marks = 2 
        else:
            marks = 1  

        
    submit_button = st.button("Submit")

    if submit_button and location:
        new_row = {"latitute": location['coords']['latitude'], "longitude": location['coords']['latitude'], "usabiluty": resusable_input , "marks_needed": marks, "urls": image_url}
        input_df.loc[len(input_df)] = new_row
        st.write("Submission received!")


    #st.write(input_df)
    


# Use the loc method to add the new row to the DataFrame

    # Returns user's location after asking for permission when the user clicks the generated link with the given text

    # The URL parts of the page
    #location_json = get_page_location()


with tab2:
    st.header("Here you can find the nearest recycling center to you")
    if not_retriev == "N/A":
        not_retriev = "metal"
    #st.write(type(location))
    lats, longs, noms, required_recycling_types = generate_recycling_locations2(sammelstellen, location, trans_dict[not_retriev])
    #st.write(lats[0])
    #st.write(longs[0])
    #st.write(noms[1])
    #st.write(required_recycling_types)
    if location:
        lon = location['coords']['longitude']
        lat = location['coords']['latitude']
        

        st.header(f"Your location is: {lon}, {lat}")





        fig = go.Figure(go.Scattermapbox(
            lat=[lat, lats[0]],
            lon=[lon, longs[0]],
            mode='markers',
            marker=go.scattermapbox.Marker(
            size=25, color=["red", "green"], 
            ),
            text=["You", noms[1]],
        ))


        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox_style="open-street-map",
            mapbox=dict(
            center=go.layout.mapbox.Center(lat = location['coords']['latitude'],
            lon = location['coords']['longitude']),
            zoom=14
        ))
        
        st.plotly_chart(fig, use_container_width=True)

        st.write(f"https://www.google.com/maps/search/?api=1&query={lats[0]},{float(longs[0])}")

        



with tab3:
    # location values hardcoded lat = 47.4335382954281
    # lon = 9.383928186686626
    # recycling center = 47.41847764687886, 9.36442953556214


    st.header("Here are some deals that are too good to throw!")
    
    # st.write(type(location))
    # st.write("Done")
    #st.write(input_df)
    if location:
        lon = location['coords']['longitude']
        lat = location['coords']['latitude']

        lat_list = list(input_df["latitute"])
        lat_list.append(lat)
        lon_list = list(input_df["longitude"])
        lon_list.append(lon)

        st.header(f"Your location is: {lon}, {lat}")
        lat_list = input_df["latitute"]
        lon_list = input_df["longitude"]
        colour_list = (["green"] * (len(lat_list) - 1))
        colour_list.insert(len(lat_list),"red")
        text_input = ["Furniture"] * (len(lat_list) - 1)
        text_input.insert(len(lat_list),"You")
        fig = go.Figure(go.Scattermapbox(
            lat = lat_list,
            lon = lon_list,
            mode='markers',
            marker={'size': 20, 'color': colour_list},
            text=text_input,
        ))


        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox_style="open-street-map",
            mapbox=dict(
            center=go.layout.mapbox.Center(lat = location['coords']['latitude'],
            lon = location['coords']['longitude']),
            zoom=14
        ))
            
    st.plotly_chart(fig,use_container_width = True)



