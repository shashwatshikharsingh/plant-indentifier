# Plant Identifier Project 🌳🌳🌸🌺🌻🌷🌻

## Introduction

Welcome to the Plant Identifier project! This project is designed to help users identify various plant species by uploading or taking pictures of plants. It uses Flask, OpenCV, Python, and Jinja to create a website that offers features such as user registration, login, logout, image recognition, and detailed plant information display.

## Features

### User Authentication

1. **User Registration**: Users can create an account by providing their username and password.

2. **User Login**: Registered users can log in to their accounts using their credentials.

3. **User Logout**: Logged-in users can log out to end their session.

### Image Recognition

4. **Image Upload**: Users can upload images of plants directly to the website.

5. **Image Capture**: Users can capture pictures of plants using their device's camera.

6. **Plant Identification**: After uploading or capturing an image, the system uses OpenCV for image processing and plant recognition to identify the plant species.

### Plant Information

7. **Plant Information Page**: Once the plant is identified, users can view detailed information about the plant, including its common name, scientific name, habitat, and more.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/shashwatshikharsingh/plant-identifier.git
   cd plant-identifier
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```


## Usage

1. Run the Flask application:
   ```
   flask run
   ```

2. Access the website in your web browser at `http://localhost:5000`.

3. Register an account, log in, and start using the plant identifier.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.

2. Clone your forked repository locally.

3. Create a new branch for your feature or bug fix.

4. Make your changes, commit, and push to your fork.

5. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Special thanks to the Bennett University Hackathon.

- Plant recognition models used in this project are based on open-source research and data.

Happy plant identifying! 🌱🌿🌸
