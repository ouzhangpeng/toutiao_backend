"""
配置模块入口 - 根据环境变量加载对应配置
"""

import os
from typing import Type

from .base import Settings
from .test import TestSettings


def get_settings_class() -> Type[Settings]:
    """根据环境变量获取配置类"""
    env = os.getenv("APP_ENV", "development").lower()

    if env == "test":
        return TestSettings
    else:
        return Settings


# 创建全局配置实例
settings = get_settings_class()()
