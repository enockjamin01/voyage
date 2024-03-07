# Voyage

This Django-based web application allows users to plan trips by fetching the coordinates of locations. The app integrates with MapBox for mapping functionalities and utilizes Firebase for user authentication and data storage.

## Setup

### Install Required Packages.

```bash
pip install -r requirements.txt
```
### Configure Firebase:
* Create a Firebase project and configure authentication for Email and Password.
* Obtain Firebase configuration credentials and update them in the Django settings.
* Add Firebase JSON file in the Main folder.
* Configure Firebase Real-Time Database

### Configure MapBox:
Sign up for a MapBox account and obtain the API key.
Update the API key in the appropriate settings file.

### Add MapBox API token / Access Token at 
```bash
voyage/maps/static/maps/scripts/maps.js
```
### Run Application
```bash
python manage.py runserver
```
## Languages and Frameworks used
* Python
* Javascript
* HTML
* CSS
* Django
* Mapbox
* Firebase


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the functionality or fix bugs.

## License

This project is licensed under the MIT License.

