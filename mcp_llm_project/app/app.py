import connexion
import os
import sys

# Add src to Python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, src_dir)

# Initialize the app
app = connexion.App(__name__, specification_dir=src_dir)

# Enable Swagger UI
app.add_api("openapi.yaml")

application = app.app

if __name__ == "__main__":
    app.run(port=8080)
