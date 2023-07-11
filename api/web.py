from flask import Flask, render_template_string, request, jsonify, Response
import pandas as pd
import googlemaps
import folium

app = Flask(__name__)

df = pd.read_excel('data/서울시 지하철역 주소,위도,경도 ver0.7.xlsx',index_col=0)

gmaps_key = "AIzaSyCElPwHnJigXm4nMaHQuayHLl0KTsuhiyo"
gmaps = googlemaps.Client(key = gmaps_key)

mapping = folium.Map(location = [df['위도'].mean(), df['경도'].mean()],
                      zoom_start = 11.5)

for n in df.index:
    if df['주소'][n] != '':
        folium.Marker([df['위도'][n], df['경도'][n]], 
                       popup = df['역명'][n]).add_to(mapping)

@app.route('/full')
def full():
    return mapping.get_root().render()

@app.route('/')
def small():
    mapping.get_root().width = '700px'
    mapping.get_root().height = '600px'
    map_html = mapping.get_root()._repr_html_()
    with open("home.html",encoding='utf-8') as f:
        html=f.read()
        num = html.find('<div class="replace">')
        html = html[:num] + map_html + html[num:]
    return html

@app.route('/search', methods=["POST"])
def search():
    keyword = str(request.data, "utf-8")
    
    # TODO :: filter keyword with regex
    
    with open("input.txt", "a") as f: # open file in append mode
        f.write(keyword) # write keyword to file
    return jsonify("입력되었습니다.")

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True) # updates every changes
