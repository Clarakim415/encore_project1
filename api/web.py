from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import googlemaps
import folium
from folium import plugins
from Map import Map

map = Map()
mapping = map.make_map()

app = Flask(__name__,static_folder='/static')

@app.route('/')
def small():
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
    app.run(debug=True) # updates every changes