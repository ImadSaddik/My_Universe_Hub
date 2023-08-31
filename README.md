# APOD Redesigned: Astronomy Picture Of the Day

Welcome to the **APOD Redesigned** repository! This project aims to improve and enhance the user experience of NASA's Astronomy Picture of the Day (APOD) website by leveraging the power of Django and Vue.js. If you're a space enthusiast who loves visualizing the cosmos through captivating images, this project will provide you with an improved interface and additional features to make your astronomical journey even more exciting.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview


The original APOD website by NASA delivers awe-inspiring astronomical images and descriptions on a daily basis. However, its interface, though informative, can feel outdated. Navigating through the website often involves clicking on multiple links to access images, which can be time-consuming and less user-friendly. This project aims to bring a fresh look and fell to the website and enhances user interaction. Our goal is to provide a seamless and visually pleasing way for users to explore and enjoy the cosmos effortlessly.

Using the power of `BeautifulSoup`, this project scrapes data from NASA's official APOD website, extracting images, titles, explanations, and other relevant information. The redesigned web application offers various pages and features to enhance user engagement.

## Features

1. **Home Page - Gallery:** Browse through an extensive gallery of astronomical images.

2. **Today's Picture:** Get the astronomy picture that was uploaded today.

3. **Trending Page:** Explore the popular images that have captured the imagination of space enthusiasts.

4. **Favorites Page:** View your favorite images that you liked.

5. **User Authentication:** Sign up and log in to the website.

6. **Image Interaction:**
   - **Like Images:** Express your appreciation for images by liking them.
   - **Download Images:** Download high-quality versions of the images for offline enjoyment.

## Installation

Follow these steps to get the project up and running:

1. Clone this repository:
   ```bash
   git clone https://github.com/ImadSaddik/apod_website_redesign.git
   ```

2. Navigate to the project directory:
   ```bash
   cd apod_website_redesign
   ```

3. Install backend dependencies (assuming you have Python and pip installed):
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   
4. Start Django:
   ```bash
   python manage.py runserver
   ```

5. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

6. Start the development server:
   ```bash
   npm run serve
   ```

## Usage

Once the project is set up, you can access the different pages through the navigation bar. Browse through the gallery, view today's picture, explore trending images, and manage your favorite images after logging in.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them.
4. Push your changes to your fork: `git push origin feature-name`.
5. Open a pull request describing your changes.

## Acknowledgements

We would like to extend our sincere gratitude to NASA for their remarkable dedication in sharing the marvels of the universe through the original Astronomy Picture of the Day (APOD) website. Their commitment to showcasing awe-inspiring astronomical images has been a constant source of inspiration for this project.

---

We hope you enjoy exploring the cosmos through the **APOD Redesigned** website. Feel free to reach out with any feedback or ideas for further improvement. Happy stargazing! 🌌🚀
