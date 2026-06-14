# 搜索源说明

这个小工具现在按“源适配器”思路做：既能接公开 API，也能接你自己部署或有权使用的网盘/目录/磁力搜索接口。

重要：不要直接用 `file://.../index.html` 打开。请双击 `start-tool.bat`，通过 `http://127.0.0.1:8766/index.html` 使用。否则浏览器会拦截很多在线源和本地代理请求。

## 已直接接入

| 源 | 主要内容 | 说明 |
| --- | --- | --- |
| GitHub 中文开源 | 中文项目、工具、资源仓库 | 使用 GitHub 仓库搜索接口，优先搜名称、描述、README。 |
| Gitee 开源项目 | 国内开源项目 | 使用 Gitee 仓库搜索接口。 |
| Hugging Face 模型 | AI 模型 | 搜模型名、标签、任务类型。 |
| Hugging Face 数据集 | 数据集 | 搜公开数据集。 |
| Hugging Face Spaces | 在线演示和应用 | 搜可用的公开 demo。 |
| npm 软件包 | JavaScript/Node 包 | 搜 npm Registry。 |
| Maven 软件包 | Java/Android 依赖 | 搜 Maven Central。 |
| Docker Hub 镜像 | 容器镜像 | 搜公开镜像。 |
| 香港开放数据 | 政府开放数据 | 搜 DATA.GOV.HK 数据集。 |
| Openverse 图片 | 开放授权图片 | 搜开放许可图片。 |
| Openverse 音频 | 开放授权音频 | 搜开放许可音频。 |
| Wikimedia Commons | 开放媒体素材 | 图片、音频、视频、文档等。 |
| Internet Archive | 公开资料、软件、媒体 | 不同网络环境下连通性会波动。 |
| Library of Congress | 馆藏资料 | 图片、地图、手稿、音视频等。 |
| Open Library / Project Gutenberg | 图书类 | 保留为补充源，不是主方向。 |
| OpenAlex / Crossref | 学术元数据 | 保留为补充源，不是主方向。 |

## 已支持的可配置外部源

| 类型 | 适合接入 | 填写方式 |
| --- | --- | --- |
| PanSou 兼容搜索 | 自建网盘搜索、插件搜索、支持磁力/ED2K/网盘类型的接口 | 接口地址填服务根地址，例如 `http://localhost:8888`。如开启认证，在令牌栏填 JWT。 |
| AList / OpenList 搜索 | 自建网盘目录、对象存储、WebDAV 聚合目录 | 接口地址填服务根地址，例如 `http://localhost:5244`。如需要认证，在令牌栏填 token。 |
| SearXNG 元搜索 | 自建综合搜索入口 | 接口地址填根地址，例如 `http://localhost:8080`。需要实例开启 JSON 输出。 |
| Torznab / Jackett / Prowlarr | 自建索引器、RSS/Torznab 搜索 | 可填完整模板，例如 `http://localhost:9117/api/v2.0/indexers/all/results/torznab/api?t=search&q={q}`，API key 可写在 URL 或令牌栏。 |
| 通用 JSON GET | 任何返回 JSON 的搜索接口 | 接口地址可用 `{q}` 作为关键词占位，例如 `https://example.com/search?q={q}`；令牌栏可填数组路径，如 `data.items`。 |

## GitHub 上值得关注的项目方向

| 项目/方向 | 用法建议 |
| --- | --- |
| `fish2018/pansou` | 适合自建网盘搜索 API，本工具已按 `/api/search` 做适配。 |
| `AlistGo/alist`、OpenList 分支 | 适合把自己的网盘、对象存储、WebDAV 统一成可搜目录。 |
| `RSSHub` | 适合把社区更新、资源站更新、论坛更新变成订阅源，再进一步入库检索。 |
| `SearXNG` | 适合自建元搜索入口。公共实例不稳定，建议自己部署。 |
| Jackett / Prowlarr | 适合接你有权使用的 Torznab 索引器，本工具已支持 Torznab XML 结果。 |
| Meilisearch / Typesense | 适合把自己的网盘清单、收藏夹、Excel 台账、站点爬取结果做成本地全文搜索。 |

## 使用建议

1. 先双击 `start-tool.bat`，通过本地服务打开工具。这样跨域接口会自动走本地代理。
2. 公开 API 源不需要配置，输入关键词直接搜。
3. 网盘/磁力/目录类源建议接你自己部署的接口，或者你确认有合法授权的接口。
4. 如果某个源很慢，工具会在约 9 秒后跳过它，不会卡住整体搜索。
5. 导出数据会包含外部源配置和令牌，导出的 JSON 请当私密配置保存。

## 参考链接

- [GitHub Search API](https://docs.github.com/en/rest/search/search)
- [Gitee OpenAPI](https://gitee.com/api/v5/swagger)
- [Hugging Face Hub API](https://huggingface.co/docs/hub/api)
- [npm Registry search](https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md)
- [Maven Central Search API](https://central.sonatype.org/search/rest-api-guide/)
- [Docker Hub API](https://docs.docker.com/docker-hub/api/latest/)
- [DATA.GOV.HK API](https://data.gov.hk/en/help/api-spec)
- [Openverse API](https://api.openverse.org/v1/)
- [PanSou](https://github.com/fish2018/pansou)
- [AList](https://github.com/AlistGo/alist)
- [RSSHub](https://github.com/DIYgod/RSSHub)
- [SearXNG Search API](https://docs.searxng.org/dev/search_api.html)
