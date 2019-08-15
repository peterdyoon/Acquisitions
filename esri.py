import requests, json, yaml
import pandas as pd

def get_token():

	account_info = yaml.load(open("/Users/peteryoon/Documents/Esri/esri_account_info.yaml", "r"))

	company_url = "https://msidecap.maps.arcgis.com/"
	url = "https://www.arcgis.com/sharing/generateToken?parameters"
	params = {
	    "username": account_info["username"],
	    "password": account_info["password"],
	    "referer": company_url,
	    "expiration": 480,
	    "f": "json"
	}

	response = requests.post(url=url, params=params)
	token = response.content.split('"token":"')[1].split('","')[0]

	with open("/Users/peteryoon/Documents/Esri/access_token.yaml", "w") as outfile:
		yaml.safe_dump(token, outfile)


def get_response(location, rings, data_types):

	token = yaml.load(open("/Users/peteryoon/Documents/Esri/access_token.yaml", "r"))

	if isinstance(location, str):
		area_details = {
			"address": {"text": location},
			"areaType": "RingBuffer",
			"bufferUnits": "esriMiles",
			"bufferRadii": rings
		}
	elif isinstance(location, list):
		area_details = {
			"geometry": {"x": location[1], "y": location[0]},
			"areaType": "RingBuffer",
			"bufferUnits": "esriMiles",
			"bufferRadii": rings
		}		
	url = 'https://geoenrich.arcgis.com/arcgis/rest/services/World/geoenrichmentserver/GeoEnrichment/enrich?studyAreas=[{}]&analysisVariables={}'.format(str(area_details), str(data_types))
	headers = {"Authorization": token}
	params = {
	    "token": token,
	    "f": "json"
	}

	response = requests.post(url=url, params=params)

	response_json = json.loads(response.content)

	try:
		field_names = response_json["results"][0]["value"]["FeatureSet"][0]["fieldAliases"]
	except:
		if "results" in response_json.keys() and len(response_json["results"][0]["value"]["FeatureSet"]) == 0:
			raise ValueError("No results; check data type.")
		elif "error" in response_json.keys():
			if response_json["error"]["code"] == 498 or response_json["error"]["code"] == 401:
				get_token()
				raise SyntaxError("Invalid token; generating new token. Try again.")
		else:
			raise ValueError("Unknown error: See json blob. >> {}".format(response_json))

	return response_json


def get_df(location, rings=[1, 2, 3], data_types=["KeyUSFacts.TOTPOP_CY", "KeyUSFacts.MEDHINC_CY"]):

	response_json = get_response(location, rings, data_types)

	values_per_ring = [value["attributes"] for value in response_json["results"][0]["value"]["FeatureSet"][0]["features"]]

	field_names = response_json["results"][0]["value"]["FeatureSet"][0]["fieldAliases"]
	final = {"Field Name":[field_names[key] for key in values_per_ring[0].keys()], "Internal Name": [key for key in values_per_ring[0].keys()]}
	for index, ring_value in enumerate(values_per_ring):
		final["Mile {}".format(ring_value["bufferRadii"])] = [value for value in ring_value.values()]

	print "ESRI Search Complete for {}".format(location)
	df = pd.DataFrame(final)

	if isinstance(data_types, list):
		short_data_types = [data.split(".")[-1] for data in data_types]
		return df[df["Internal Name"].str.contains("|".join(short_data_types))]
	elif isinstance(data_types, str):
		short_data_types = data_types.split(".")[-1]
		return df[df["Internal Name"] == short_data_types]
	else:
		raise SyntaxError("Make sure data types are correct.")
	


def get_value(location, ring=1, data_type="KeyUSFacts.TOTPOP_CY"):

	if isinstance(ring, list) or isinstance(data_type, list):
		raise SyntaxError("Ring or data type is a list; remove brackets --> []")

	response_json = get_response(location, [ring], [data_type])

	short_data_type = data_type.split(".")[-1]

	return response_json["results"][0]["value"]["FeatureSet"][0]["features"][0]["attributes"][short_data_type]
















