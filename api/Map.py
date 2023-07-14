import pandas as pd
import googlemaps
import folium
from folium import plugins

class Map:
    def __init__(self):
        self.df = pd.read_excel('data/서울시 지하철역 주소,위도,경도 ver0.7.xlsx',index_col=0)
        self.station_df = pd.read_excel('data/서울시 지하철역 주소,위도,경도 ver0.7.xlsx')
        self.restroom_df = pd.read_csv('data/역별 화장실 주소.csv')
        self.store_df = pd.read_csv('data/역별 편의점 주소.csv')
        # pharmacy_df = pd.read_csv('data/역별 약국 주소.csv')
        # bank_df = pd.read_csv('data/역별 은행 주소.csv')

        self.gmaps_key = "AIzaSyCElPwHnJigXm4nMaHQuayHLl0KTsuhiyo"
        self.gmaps = googlemaps.Client(key = self.gmaps_key)
        
        self.mapping = folium.Map(location = [self.df['위도'].mean(), self.df['경도'].mean()],
                        zoom_start =14)

    def popup_text(self,station):
        data = pd.read_csv('data/서울시 지하철 엘레베이터랑 에스컬레이터 출구정보.xlsx',index_col=0)
        
        if station not in list(data.역명.values):
            return '<pre>' + station + '역\n' + '</pre>'
        
        data['엘레베이터 위치'] = data['엘레베이터 위치'].apply(lambda cell:''.join(c for c in cell if c not in "'[]").split(', '))
        data['에스컬레이터 위치'] = data['에스컬레이터 위치'].apply(lambda cell:''.join(c for c in cell if c not in "'[]").split(', '))
        
        elev = list(data[data['역명'] == station]['엘레베이터 위치'])[0]
        elev_loc = ', '.join(loc for loc in elev)
        
        esc = list(set(list(data[data['역명'] == station]['에스컬레이터 위치'])[0]))
        esc_loc = ', '.join(loc for loc in esc)
        
        html = '<h2>' + station + '역</h2><br><h6>' + '엘레베이터: ' + elev_loc + '</h6><br><h6>' + '에스컬레이터: ' + esc_loc +'</h6><br>'
        return html
    
    def marker(self,df,color,icon,group=None):
        for n in df.index:
            if icon=='subway':
                popup = folium.Popup(self.popup_text(df['역명'][n]), min_width=100, max_width=200)
                folium.Marker([df['위도'][n], df['경도'][n]], 
                            popup = popup,
                            icon = folium.Icon(
                                color=color,
                                icon=icon,
                                prefix ='fa'),
                            tooltip = df['역명'][n]
                            ).add_to(self.mapping)
            else:
                restroom_review = pd.read_csv('data/화장실 별점.csv',index_col=0)
                restroom_review.dropna(how='any')
                name = df['이름'][n]
                if (icon=='restroom') and (name in list(restroom_review.이름.values)):
                    html = '<h4>' + name + '</h4><br><h6>' + '별점: ' + str(list(restroom_review[restroom_review['이름'] == name]['별점'])[0]) +'</h6><br>'
                    popup = folium.Popup(html, min_width=100, max_width=200)
                else:
                    html = '<h5>' + name + '</h5>'
                    popup = folium.Popup(html, min_width=100, max_width=200)
                
                folium.Marker([df['위도'][n], df['경도'][n]], 
                            popup = popup,
                            icon = folium.Icon(
                                color=color,
                                icon=icon,
                                prefix ='fa')
                                ).add_to(group)
    
    def make_map(self):
        for n in self.df.index:
            if self.df['주소'][n] != '':
                folium.Marker([self.df['위도'][n], self.df['경도'][n]], 
                            popup = self.df['역명'][n]).add_to(self.mapping)
                
        # 그룹별 나누기
        fg = folium.FeatureGroup(name='편의시설 보기')
        self.mapping.add_child(fg)

        restroom_group = plugins.FeatureGroupSubGroup(fg, '화장실')
        store_group = plugins.FeatureGroupSubGroup(fg, '편의점')
        # bank_group = plugins.FeatureGroupSubGroup(fg, '은행')
        # pharmacy_group = plugins.FeatureGroupSubGroup(fg, '약국')
        self.mapping.add_child(restroom_group)
        self.mapping.add_child(store_group)
        # mapping.add_child(bank_group)
        # mapping.add_child(pharmacy_group)

        

        self.marker(self.station_df,'purple','subway') # 지하철 역
        self.marker(self.restroom_df,'blue','restroom',restroom_group) # 화장실
        self.marker(self.store_df,'gray','store-alt',store_group) # 편의점
        # marker(bank_df,'cadetblue','university',bank_group) # 은행
        # marker(pharmacy_df,'red','first-aid',pharmacy_group) # 약국

        # 미니맵
        minimap = plugins.MiniMap()
        self.mapping.add_child(minimap)

        folium.LayerControl(collapsed=False).add_to(self.mapping)

        # 맵 사이즈 조정
        self.mapping.get_root().width = '900px'
        self.mapping.get_root().length = '600px'
        
        return self.mapping