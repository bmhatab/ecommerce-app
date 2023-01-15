# Ecommerce Website

A fully functional ecommerce website built using Flask, featuring an admin page for managing services and products on the website, as well as an add to cart system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Flask
- virtualenv (optional but recommended)

### Installing
 - Install the required packages:
 - pip install -r requirements.txt
 
 ####Set the environment variables:
  In command line :
  - set FLASK_APP = manager.py
  
 ##### Run the app:
  - flask run
  
  ### Usage

- To access the admin page, navigate to '/admin' and login using the provided credentials.
- To add a product or service to the website, use the 'Add Product/Service' button on the admin page.
- To view and manage existing products and services, use the 'Manage Products/Services' button on the admin page.
- To add items to the cart, use the 'Add to Cart' button on the product page.

## Deployment

This website can be deployed on a production server using a WSGI server like Gunicorn.

## Built With

* [Flask]
* [Bootstrap] - The CSS framework used

## Authors

* **Serendi** - (https://github.com/bmhatab)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
  
