from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./thegoblin-key.json')

translate_client = translate.Client(credentials=credentials)
#Text can also be a sequence of strings, in which case this method will return a sequnce of results for each text
result = translate_client.translate("刘海", target_language="en", source_language="cn")

print(result)

results = translate_client.get_languages()