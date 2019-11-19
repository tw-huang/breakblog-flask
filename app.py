from breakblog import create_app
import os
from dotenv import load_dotenv

# 导入环境变量.env和.flaskenv
dotenv_env_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv_flaskenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_env_path):
    load_dotenv(dotenv_env_path)
if os.path.exists(dotenv_flaskenv_path):
    load_dotenv(dotenv_flaskenv_path)

# 从breakblog包导入
app = create_app()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
