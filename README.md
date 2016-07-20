# The RECAST API SDK

This is a python API SDK to interact with the API hosted at
http://recast-rest-api.herokuapp.com

## Usage

POST methods require tokens, the interface at http://recast-frontend.herokuapp.com/profile can be used to retrieve a token

Set your API credentials:

````python
	import recastapi
	recastapi.ORCID_ID = 'YOUR_ORCID_ID'
	recastapi.ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

	recastapi.analysis.get.analysis() #list all analyses

	recastapi.request.get.request() #list all requests
````

## Basic Usage

(See http://cbora.github.io/recast-api/recastapi.html#module-recastapi for documentation)

