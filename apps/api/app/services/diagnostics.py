def explain_error(code: str):
    mapping = {
        'API_HEALTH_FAIL': ['检查 pm-api 是否运行', '检查 APP_BASE_URL 是否正确', '检查 8080 端口'],
        'DOCKER_NOT_RUNNING': ['执行 systemctl restart docker', '检查 docker ps'],
        'NODE_UNHEALTHY': ['检查端口和防火墙', '检查 SNI 或伪装域名', '必要时切换到其他协议'],
        'DB_WRITE_FAILED': ['检查 data 目录权限', '检查磁盘空间', '检查 SQLite 文件锁'],
    }
    return mapping.get(code, ['查看日志', '检查配置', '执行健康检查'])
