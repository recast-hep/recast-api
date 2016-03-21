# The RECAST API SDK

This is a python API SDK to interact with the API hosted at
http://recast-rest-api.herokuapp.com

As RECAST is a community project, we are moving to GitHub for collaborative development.
RECAST packages (eg. API wrappers, back-end implementations etc.) should be in repositories named recast-\<package\>

## Usage

Get  a token from http://recast-frontend.herokuapp.com/profile
Set your API credentials:

````python
	import recastapi
	recastapi.ORCID_ID = 'YOUR_ORCID_ID'
	recastapi.ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

	recastapi.analysis.analysis() #list all analyses
````