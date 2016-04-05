# The RECAST API SDK

This is a python API SDK to interact with the API hosted at
http://recast-rest-api.herokuapp.com

## Usage

Get  a token from http://recast-frontend.herokuapp.com/profile
Set your API credentials:

````python
	import recastapi
	recastapi.ORCID_ID = 'YOUR_ORCID_ID'
	recastapi.ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

	recastapi.analysis.analysis() #list all analyses
````