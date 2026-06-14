# Resource Search Tool

一个本地运行的资源搜索工具，支持直连接口、可配置搜索源、收藏、导入导出，以及 GitHub Release 自动更新。

## Start

Windows 上双击：

```text
start-tool.bat
```

程序会启动本地服务并自动打开浏览器。不要直接双击 `index.html` 使用，因为很多搜索接口会被浏览器跨域限制拦住。

## Sources

内置源偏向公开、可合法访问的接口。你也可以在界面里添加自己部署或自己有权访问的源：

- PanSou compatible `/api/search`
- AList / OpenList `/api/fs/search`
- SearXNG JSON
- Torznab / Jackett / Prowlarr
- Generic JSON GET

更多配置说明见 `SEARCH_SOURCES.md`。

## Auto Update

当前版本信息在 `app-version.json`：

```json
{
  "version": "1.0.0",
  "manifest_url": "https://github.com/wululuhaamo-spec/resource-search-tool/releases/latest/download/latest.json"
}
```

启动时会按这个流程更新：

```text
current version -> remote version -> download -> SHA256 check -> replace -> restart
```

发布新版本时，在 GitHub 创建形如 `v1.0.1` 的 tag。仓库里的 GitHub Actions 会自动打包 zip、生成 `latest.json`，用户下次启动就会检测到更新。

## Notes

这个工具保留“可扩展搜索源”的能力，但不会内置未经授权的第三方站点规则。你可以在本地添加自己部署、授权访问或合规使用的聚合接口。
