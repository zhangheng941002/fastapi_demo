#### 一、最基础的依赖
```
pip install fastapi
pip install uvicorn
```




pip install daphne


docker run -it -p 14000:8000  -v /data/start_study/:/start_study  --name asgi_test python:3.7.1 sh -c "cd /start_study && pip3 install -r requirement_asgi.txt && daphne -b 0.0.0.0 -p 8000 start_study.asgi:application"


docker run -it -v /data/start_study/:/start_study  --name asgi_test_celery python:3.7.1 sh -c "cd /start_study && pip3 install -r requirement_asgi.txt && celery  worker -A start_study  -l info -c 4"



运行asgi
	方法一：
		daphne -b 0.0.0.0 -p 8000 start_study.asgi:application  # 没有发现reload方法！
	方法二：
		uvicorn start_study.asgi:application --host 0.0.0.0 --port 8000 --workers 4 --reload   # 加入reload时，感觉workers没有了！！！！












# fastapi
pip install fastapi
pip install uvicorn


run:
	 uvicorn main:app --reload --host 0.0.0.0 --port 9090  # --workers 4   如果有reload，则该参数失效