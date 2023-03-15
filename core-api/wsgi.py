from dotenv import load_dotenv
load_dotenv(override=False)
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=4200, debug=True, threaded=True)
else:

    g_app = create_app()
