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

	recastapi.analysis.analysis() #list all analyses
````
## Commonly used functions
#### Request:
* Get request

```python
	
	request(uuid=None)
		
		"""
		Returns request data associated to ID in JSON format.
		If none returns all requests.
		"""
```

* Get parameter	

``` python
	
	parameter(request_id, parameter_index=None) 
		
		"""
		Returns the parameter associated to a given request,
		or returns all parameter if there no parameter_index provided.
		Coordinates and files are included in the returned JSON object.
		"""
```

* Get coordinate

```python			
	coordinate(request_id, parameter_index=0, coordinate_index=None)
		
		"""
		Returns the coordinate associated to a given parameter in a given request
		or returns all coordinates if no *coordinate_index* is provided.
		"""
```

* Download file

``` python				
	
	download(request_id, point_request_index=0, basic_request_index=0, download_path=None, dry_run=False)
			
		"""
		Downloads the associated file to the given parameters.
		
		Args:
		>>> request_id :: ID of the request.
		>>> point_request_index:: Analogous to the parameter index.
		>>> basic_request_index: Indexing of the file in the parameter.
		>>> dry_run: When False downloads file, 
			otherwise download link is included in the returned JSON obj.
			
		"""
``` 
		
* Prints the parameter and coordinate indices and contained data

```python
	request_tree(request_id)
```

* Creates a new request

```python
	create(analysis_id,
        	title,
	       	description_model,
	       	reason_for_request,
	       	additional_information,
	       	status="Incomplete",
	       	file_path=None,
	       	parameter_value=None,
	       	parameter_title=None)
	       	
		"""
		Creates a requests.
		
		Args:
		>>> analysis_id: ID of the analysis.
		>>> description_model: Detailed description of the model to use.
		>>> reason_for_request: Reason for submitting this request.
		>>> additional_information: Any other additional information associated to this request.
		>>> status: Defaults to Incomplete.
		>>> file_path: File to be associated with this request, optional variable.
		>>> parameter_value: Value of the scan parameter, optional
		>>> parameter_title: Optional title of the parameter title.
			
		Returns:
			JSON object with data added.
		"""
           	
```
    
* Add new parameter to a request

```python
	
	add_parameter(request_id, coordinate_value, coordinate_title=None, filename=None)
	        
		"""
		Add a parameter point to a request.
		
		Args:
		>>> request_id: ID of the request to be associated to this parameter point.
		>>> coordinate_value: Value of the scan coordinate.
		>>> parameter_title: Optional title of the scan title.
		>>> filename: Optional file path to file to associate to this parameter point.
		
		Returns:
		   JSON object with data added.
		   
		"""
```

* Add coordinate to parameter
    
```python	
	
	add_coordinate(parameter_id, coordinate_name, coordinate_value)

		"""
		Adds coordinate given parameter id.
		
		Args: 
		>>> parameter_id: analogous to point_request_id.
		>>> coordinate_value: value of the coordinate.
		>>> coordinate_name: name of the coordinate.
		
		Returns:
		   JSON object with added data
		"""
```
	
