# pip install pymysql sqlacodegen
import os
import subprocess
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# 创建数据库引擎
db_host = os.getenv("MYSQL_HOST", "localhost")
db_port = int(os.getenv("MYSQL_PORT", "3306"))
db_name = os.getenv("MYSQL_DATABASE", "ecs")
db_user_name = os.getenv("MYSQL_USER", "your_mysql_user")
db_password = os.getenv("MYSQL_PASSWORD", "")
url = os.getenv("MYSQL_URL") or (
    f"mysql+pymysql://{quote_plus(db_user_name)}:{quote_plus(db_password)}"
    f"@{db_host}:{db_port}/{db_name}?charset=utf8"
)

# 配置会话工厂
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


if __name__ == "__main__":

    def export_db_table_class(run=False):
        """将数据库表映射为Python类"""
        if not run:
            return
        output_path = "db_table_class.py"

        cmd = ["python", "-m", "sqlacodegen", url]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)

    export_db_table_class(True)
