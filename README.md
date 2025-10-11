# Little Lemon API


## English

This is a Django REST API for managing the actions performed in the e-shop of the Little Lemon restaurant.  
It allows registration and login of different user roles (Customer, Manager, Staff, Admin) with specific permissions for each role.

## Technologies used
- Python
- Django
- Django REST Framework (DRF)

## Prerequisites
- Python 3.10 or higher installed
- pip package manager

## Instructions to test the API

- Clone the repository
```bash
git clone https://github.com/AlbertoBarradas/LittleLemonAPI.git
```
- Move to the repo directory
```bash
cd LittleLemonAPI
```

- Create virtual environment (optional but recommended)

```bash
python -m venv venv
```
On Linux/Mac
```bash
source venv/bin/activate
```
On Windows

```bash
venv\Scripts\activate
```

- Install dependencies
```bash
pip install -r requirements.txt
```

- Move to the project directory and run the server
```bash
cd LittleLemon
```
```bash
python manage.py runserver
```

## Testing the API
To test the API, you can use Postman with a collection provided in the **docs** directory, this way the testing of the endpoints have been simplified.

Import the collection in Postman and perform the requests in order.

##


## Español

Esta es una API hecha en Django Rest para el manejo de las diversas acciones que se efectuan en la tienda digital del restaurante Little Lemon.
Permite el registro y el inicio de sesión para los diferentes roles de usuarios (Comprador, Manager, Staff y Administrador) con permisos especificos para cada uno.

## Tecnologías usadas
- Python
- Django
- Django REST Framework (DRF)

## Prerequisitos
- Python 3.10 o mayor instalado
- Manejador de paquetes pip

## Instrucciones para probar la API

- Clonar el repositorio
```bash
git clone https://github.com/AlbertoBarradas/LittleLemonAPI.git
```
- Mover al directorio del repositorio
```bash
cd LittleLemonAPI
```

- Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
```
En Linux/Mac
```bash
source venv/bin/activate
```
En Windows

```bash
venv\Scripts\activate
```

- Instalar dependencias
```bash
pip install -r requirements.txt
```

- Mover al directorio del proyecto y ejecutar el servidor
```bash
cd LittleLemon
```
```bash
python manage.py runserver
```

## Probar la API
Para probar la API, puedes usar Postman con una colección que se incluye en la carpeta **docs**, de esta manera se simplifica el testeo de los endpoints.

Importa la colección en Postman y ejecuta las peticiones en orden.

## Author
Alberto Barradas