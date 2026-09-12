from app import create_app
from app.config import ProductionConfig

app = create_app(ProductionConfig)

def handler(request, response):
    return app(request.environ, response.start_response)
