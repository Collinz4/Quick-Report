# Quick-Report
A simple QR code reporting tool that doesn't require sign on for reporters.

# Architecture
The application uses a variety of layers to allocate responsibilites to function calls. To keep responsibilities enforced, layers can only call the layer on the same or one level below itself. One exception to this rule is that models can be used to tranfer data to whichever layer requires it. For example: the controller can create an Asset object and pass it down to the service layer. Such action essentially uses the model as a Data Transfer Object (DTO).

## Controller (aka Flask blueprints)
Handles routing and basic data parsing from the URL request. Once the data has been extracted a service layer call may be done to handle the request further (such as getting information from the database). This layer is responsible for also rendering the correct HTML/Jinja2 template and returning a proper reponse code.

## Service
Handles authentications and database interactions. Most of the information being passed down from the controller layer needs to be sanitized in this layer before querying the database. This layer may also handle external API calls or other business logic.

## Model
This layer is responsible for modeling the database and mapping objects to tables. Much of the work is done using SQLAlchemy and nothing much should change in this layer. If the database is modifed this layer needs to reflect the changes.
