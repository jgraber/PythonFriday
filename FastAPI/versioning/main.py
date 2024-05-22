from fastapi import FastAPI

from fastapi_versionizer.versionizer import Versionizer, api_version


app = FastAPI(
    title='test',
    redoc_url=None
)


@app.get('/status')
def get_status() -> str:
    return 'Ok'


@api_version(1)
@app.get('/hello', deprecated=True)
def hello() -> str:
    return "Hello"


@api_version(2)
@app.get('/hello')
def hello_v2() -> str:
    return "Hi"


versions = Versionizer(
    app=app,
    prefix_format='/v{major}',
    semantic_version_format='{major}',
    latest_prefix='/latest',
    sort_routes=True
).versionize()