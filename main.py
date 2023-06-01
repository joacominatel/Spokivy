import spotipy
import webbrowser
from spotipy.oauth2 import SpotifyOAuth
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.utils import escape_markup
from kivy.graphics import Color, Rectangle


# Datos de autenticación de Spotify
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = '/'

class SongButton(ButtonBehavior, Label):
    pass

class SpokivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Sección de búsqueda
        search_layout = BoxLayout(size_hint=(1, 0.1), padding=(10, 10, 10, 10))
        search_box = TextInput(hint_text='Escriba un artista...', size_hint=(0.7, 1))
        search_box.background_color = (1, 1, 1, 1)  # Color de fondo blanco
        search_box.border = (10, 10, 10, 10)  # Bordes redondeados
        search_layout.add_widget(search_box)
        
        # Botón de configuración
        dropdown = DropDown()
        btn_config = Button(text='Configuración', size_hint=(0.3, 1))
        btn_config.background_color = (0, 0.5, 0, 1)  # Color de fondo verde oscuro
        btn_config.bind(on_release=lambda btn: dropdown.open(btn))
        search_layout.add_widget(btn_config)
        layout.add_widget(search_layout)
        
        # Opciones de configuración en el menú desplegable
        menu_options = ['Logout']
        for option in menu_options:
            btn_option = Button(text=option, size_hint_y=None, height=40)
            btn_option.bind(on_release=lambda btn: self.process_config_option(btn.text))
            dropdown.add_widget(btn_option)
        
        # Sección de respuesta
        response_label = Label(text='', size_hint=(1, 0.7))
        response_label.background_color = (0, 0, 0, 1)  # Color de fondo negro
        response_label.color = (1, 1, 1, 1)  # Color de texto blanco
        layout.add_widget(response_label)
        
        # Sección de botones
        buttons_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        
        buttons_row1 = BoxLayout(size_hint=(1, 0.5))
        buttons_row1.add_widget(Button(text='Imprimir las canciones más escuchadas', on_release=lambda btn: self.print_top_songs(response_label)))
        buttons_row1.add_widget(Button(text='Tus playlists', on_release=lambda btn: self.show_playlists(response_label)))
        buttons_row1.add_widget(Button(text='Actualmente escuchando...', on_release=lambda btn: self.show_currently_playing(response_label)))
        
        buttons_row2 = BoxLayout(size_hint=(1, 0.5))
        buttons_row2.add_widget(Button(text='Artistas más escuchados', on_release=lambda btn: self.show_top_artists(response_label)))
        buttons_row2.add_widget(Button(text='Recomendar canciones', on_release=lambda btn: self.show_recommendations(response_label)))
        
        buttons_layout.add_widget(buttons_row1)
        buttons_layout.add_widget(buttons_row2)
        layout.add_widget(buttons_layout)
        
        return layout
    
    def process_config_option(self, option):
        if option == 'Logout':
            # Aquí puedes agregar la lógica para borrar la cuenta del archivo de caché
            print('Logout')

    def print_top_songs(self, label):
        top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')

        # Reiniciar el contenido del label
        label.text = ''

        for idx, track in enumerate(top_tracks['items'], start=1):
            artists = ', '.join([artist['name'] for artist in track['artists']])
            song_info = f"{idx}. {track['name']} - {artists}"
            label.text += song_info

            # Agregar un espacio entre las canciones
            if idx < len(top_tracks['items']):
                label.text += '\n\n'

        # Alinear el texto a la izquierda
        label.text_size = (label.width, None)
        label.halign = 'left'
        label.padding = [10, 0, 0, 0]

    
    def show_playlists(self, label):
        playlists = sp.current_user_playlists()
        label.text = ''
        
        for idx, playlist in enumerate(playlists['items'], start=1):
            playlist_name = playlist['name']
            label.text += f"{idx}. {playlist_name}\n\n"
        
        label.text_size = (label.width, None)
        label.halign = 'left'


    def show_currently_playing(self, label):
        current_track = sp.current_user_playing_track()
        
        # Reiniciar el contenido del label
        label.text = ''
        
        if current_track is not None and 'item' in current_track:
            track_name = current_track['item']['name']
            artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
            label.text = f"Actualmente escuchando:\n{track_name} - {artists}"
        
        # Alinear el texto a la izquierda
        label.text_size = (label.width, None)
        label.halign = 'left'


    def show_top_artists(self, label):
        top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
        
        # Reiniciar el contenido del label
        label.text = ''
        
        for idx, artist in enumerate(top_artists['items'], start=1):
            artist_name = artist['name']
            artist_uri = artist['external_urls']['spotify']
            
            # Crear botón para el enlace al artista
            link_button = Button(text='Link', size_hint=(None, None), size=(70, 30))
            link_button.bind(on_release=lambda btn, uri=artist_uri: self.open_spotify_page(uri))
            
            # Agregar el fondo verde al botón
            with link_button.canvas.before:
                Color(0, 0.5, 0, 1)  # Color verde oscuro (R, G, B, A)
                Rectangle(pos=link_button.pos, size=link_button.size)
            
            label.text += f"{idx}. {artist_name}"
            label.add_widget(link_button)
            label.text += '\n\n'
        
        # Alinear el texto a la izquierda
        label.text_size = (label.width, None)
        label.halign = 'left'

    def open_spotify_page(self, uri):
        webbrowser.open(uri)

    def show_recommendations(self, label):
        # Aquí puedes agregar la lógica para mostrar las recomendaciones de canciones en el cuadro de respuesta
        label.text = 'Recomendar canciones'
    
if __name__ == '__main__':
    # Configuración de autenticación de Spotify
    sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read,user-library-read,user-read-currently-playing, playlist-modify-public, playlist-modify-private, user-library-modify"
    )
)    
    # Ejecución de la aplicación Spokivy
    SpokivyApp().run()
