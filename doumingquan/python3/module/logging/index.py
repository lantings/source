import logging

logger = logging.getLogger(__name__)

# 终端打印info信息
logging.basicConfig(format='%(asctime)s: %(message)s',level=logging.ERROR)
logger = logging.getLogger(__name__)
# level对应下面的方法
logger.error("this is error ")

logging.basicConfig(format='%(asctime)s: %(message)s',level=logging.INFO)
# level对应下面的方法
logging.info("this is info")

logging.basicConfig(format='%(asctime)s: %(message)s',level=logging.DEBUG)
# level对应下面的方法
logging.debug("this is debug")

logging.basicConfig(format='%(asctime)s: %(message)s',level=logging.CRITICAL)
# level对应下面的方法
logging.critical("this is critical")












