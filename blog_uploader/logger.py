import logging
import os
from datetime import datetime

def setup_logger():
    # 创建logs目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志文件名（使用当前日期）
    log_file = os.path.join(log_dir, f'blog_uploader_{datetime.now().strftime("%Y%m%d")}.log')
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('blog_uploader') 