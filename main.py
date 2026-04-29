from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import news, users, favorite, history
from utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册异常

register_exception_handlers(app)


# 跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,  # cookie
    allow_methods=["*"],  # 请求方法
    allow_headers=["*"],  # 请求头
)


# 挂载，把路由注入类似 include_router(文件.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
