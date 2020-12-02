from mangum import Mangum

from fastapi_lambda.app import app


handler = Mangum(app)