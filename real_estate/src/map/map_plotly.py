from real_estate.src.database.firebase_manager import connect_to_firebase, get_firebase_data


connect_to_firebase()
data = get_firebase_data('Consolação, São Paulo, SP')
print(data)
