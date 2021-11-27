from firebase_admin import db
import firebase_admin


def _connect_to_firebase(api_key: dict, database_url: str):
    if not firebase_admin._apps:
        cred_obj = firebase_admin.credentials.Certificate(api_key)
        firebase_admin.initialize_app(cred_obj, dict(databaseURL=database_url))


def connect_to_firebase() -> None:
    api_key = {
        "type": "service_account",
        "project_id": "real-estate-scrapper-2ac0c",
        "private_key_id": "38f877fa36e5fef7a6ca6267d977605a6f116d4d",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDE3NEqpllPha/q\nLRwsRUfwWWsC5aAJC0tK3NtBeYid7x4GPOPwb2SIChdo19Ft7GxNDx/3fIPHhoKn\nZyxfrvU5/64SXdRnfJP2/sdipcxdrA+EXnzYRvvfvh55RBt5iqeeN6ggJMhql267\nenvMuVGa4J6WyJpqM3+iUUcKnNOcfMTLAQ/gzQEqB1b6KScPK2GkM4SZCgktEy5L\nlxfXnq7wYv+TLR6H9nFueKvhDMq/WDl+JOS3ChExMa5HQ+Yp83AByKGQJ2gVlYia\nWebWhPd6yU3ArcZS8wUJsJY3Io5iQ+//SNA7ELHP123n96j2rGzroStoagdCXdox\nW9jDfnNfAgMBAAECggEAMkc7XKszsC2yqhpvUZc4MliEDi9bWjP6PNp/XQ+PJtcF\nUg6HIMcyY9Q/+lT0diCl4GB2h5zTg0gFYn/lQ2LJ2tBEQwiX0P5uQ+z6O2Wg9mOV\navc+53XpqlFCMzKD2dzhxnTsiZkbXq3iaBt2Nuk1wFqR5mzBk1InzOr5O+ql2RdJ\n0B3EiDi9qUSpei1eGrDLvQ4llfl07afOPGv3980yBQ1nhMkWabKY1d3lH6X21wYU\n4LvOjaYkrTB20UE7/6jEsSAMTKGTpeK5AchfI2eBr9SQJ8My4RrusytMrctaq31u\nYgsGkTwMn2ZbsOd8miwffT4DjcR4qUXSPkOGi5tlEQKBgQDsdU9ZzuS41ZIegUzj\n7Y2ecrEfkHDX5t9yt+LIoYjmZSVMRc7G4LwvKrdSUZD6PjxH/bdE7y7QpFaBuoDC\n9G3koGEzeCZHrQMIdY+AVWx5WQuOMjrkU7uihuIo2fwFPwXaQ/DualhP+MOeeWLr\n2NgL/tofps2MIQAEv9k3bLp5JQKBgQDVIcp6e4rlV/CqrcwTiKg3pfa3ElcjCIX1\nNAyVYtmGjzn1tU0KjobYgtlwWziKp4PTTDuXYIQRe9yckkR6xZ11scfi31r2Yyb/\nM/jpjSNN9tImwk6f+yaf/lM3etJJSQyQKEew7hOKMhCcwdOThUVRlDL7jCQjEXvB\n3XZxgsi9MwKBgCFyPnUflK6oVvDFrVCYK238Hx2t2qhPWc/qPsPORYUBTZNKVINB\nCp1JV4DnVLBw2Sn9s0ym4GJWvH3BGbF5zYmHPfh/yDpfOIybxF6Mtrk7ZS0J4dam\nGWZV2euZWdKMJZHIBm5S0IcPUuw5k0p086pOtB/CAlUN3ejOEjWKxZ2ZAoGAbUvO\n0dDZAZN/T4egx8OkwCTTyD4XgVe1mnD+ovz2IBMC3gYDZA6DCDTR3NRqwm/1Ij5N\nsOtFztF96Kz5gRwmC10H7EguFXvzW5wDYYGHQUv5qPar606YGCQL+L97ZymWz7ZY\nTVtJmeziqACdx2Dok1U0b9sGDRXCKUCwpLU0zBECgYEA0Bbb3InNEhxQ5Wzr+4xI\ne5g9aR+4doNBQfn34/Wsdb1zdKPp2h/rFa1BYtMAUefH+Vb1i0PSNetmPG/QWZev\nYWxEkP/oFtzFT2IEIaiHOW8T7Vp5LEKeKRVligxBRRFFEuqhcePTFqTTmruM/kbz\nN8Ps+7zaY6kngfWP3/ieMtM=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-61a5m@real-estate-scrapper-2ac0c.iam.gserviceaccount.com",
        "client_id": "108396751058577278801",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-61a5m%40real-estate-scrapper-2ac0c.iam.gserviceaccount.com"
    }
    database_url = "https://real-estate-scrapper-2ac0c-default-rtdb.firebaseio.com/"
    _connect_to_firebase(api_key, database_url)


def upload_json_to_firebase(
        json_data: dict, address: str,
        api_key: dict = None, database_url: str = None, is_new=True):
    try:
        if api_key and database_url:
            _connect_to_firebase(api_key, database_url)
    except ValueError:
        pass
    ref = db.reference(address)

    # with open(json_file_path, "r") as f:
    #     file_contents = json.load(f)
    if is_new:
        ref.set(json_data)


def get_firebase_data(address: str, api_key: dict = None, database_url: str = None):
    try:
        if api_key and database_url:
            _connect_to_firebase(api_key, database_url)
    except ValueError:
        pass
    ref = db.reference(address)
    return ref.get()

