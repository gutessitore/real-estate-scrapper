import folium
from src.main import connect_to_firebase
from src.database.firebase_manager import get_firebase_data


connect_to_firebase()
data = get_firebase_data('Perdizes')
print(data)
