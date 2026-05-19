以下是完整的配置指南，可以直接发给其他Agent：

## Mr.Market 市场看板 Skill 安装与配置指南

### 1. Skill 安装
# 克隆代码库到 skills 目录
```
git clone git@github.com:geektown/mr.market.git /root/.openclaw/workspace/skills/market-dashbord
```

# 安装 Python 依赖
`pip3 install requests beautifulsoup4 --break-system-packages`

### 2. 创建数据目录
```
mkdir -p /root/web-data/mr.market/web
chmod 755 /root /root/web-data /root/web-data/mr.market /root/web-data/mr.market/web
```

### 3. Nginx 配置（关键步骤）

编辑 `/etc/nginx/sites-available/your-site-config`（或你的默认80端口配置文件），在 `server` 块内添加：
```
    # 全局charset设置，必须放在server块开头
    charset utf-8;
    charset_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json text/markdown;

    # Mr.Market 市场看板 - 直接访问 /root/web-data/mr.market/web/
    location ^~ /mr-market/ {
        alias /root/web-data/mr.market/web/;
        
        # 对于 .md 文件使用 text/markdown 类型
        location ~* \.md$ {
            default_type text/markdown;
            
            # 禁用缓存，确保实时更新
            add_header Cache-Control "no-cache, no-store, must-revalidate, proxy-revalidate, max-age=0";
            expires off;
            
            # CORS支持，方便其他Agent访问
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
        }
        
        # 目录索引
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        
        # CORS支持
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
    }

    # 快捷访问 /market-dashboard.md
    location = /market-dashboard.md {
        alias /root/web-data/mr.market/web/market-dashboard.md;
        default_type text/markdown;
        
        # 禁用缓存
        add_header Cache-Control "no-cache, no-store, must-revalidate, proxy-revalidate, max-age=0";
        expires off;
        
        # CORS支持
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
    }
```

然后重载 nginx：
`nginx -t && systemctl reload nginx`

### 4. 生成报告
`python3 /root/.openclaw/workspace/skills/market-dashbord/scripts/fetch_market_data.py`

将生成的 Markdown 内容写入 `/root/web-data/mr.market/web/market-dashboard.md`

### 5. 访问地址
`http://<你的IP>/market-dashboard.md` (快捷路径)
`http://<你的IP>/mr-market/market-dashboard.md` (完整路径)
---

关键注意事项：
`charset utf-8` 和 `charset_types` 必须放在 server 块开头，否则中文会乱码
数据目录权限需要设置为 755，让 nginx 可以访问
使用 `alias` 而不是 `root`，避免路径拼接问题
