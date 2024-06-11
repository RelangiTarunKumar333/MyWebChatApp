# Flask Chatbot Application

This is a simple Flask web application with user authentication and a chatbot interface. The application fetches images from Pexels and videos from YouTube based on the user's chat input.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/flask-chatbot-app.git
    cd flask-chatbot-app
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    Rename the `.env2` file to `.env` and fill in your API keys:

    ```bash
    mv .env2 .env
    ```

5. Run the application:

    ```bash
    flask run
    ```

## Usage

- Navigate to `http://127.0.0.1:5000` in your web browser.
- Register a new user or log in with an existing account.
- Start chatting with the bot.

## Folder Structure

- `my_app.py`: Main application file
- `templates/`: HTML templates for the application
- `static/`: Static files (CSS, JS)
- `.env2`: Environment variables file

## License

This project is licensed under the MIT License.
