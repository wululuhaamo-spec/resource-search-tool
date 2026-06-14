# Resource Search Tool

一个本地运行的资源搜索工具，支持直连接口、可配置搜索源、源订阅自动刷新、收藏、导入导出，以及 GitHub Release 自动更新。

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

## Source Subscriptions

这个工具尽量把“程序更新”和“源更新”分开。程序本体是稳定底座，源列表可以远程刷新。

默认订阅：

```text
https://raw.githubusercontent.com/wululuhaamo-spec/resource-search-tool/main/sources/source-registry.json
```

打开工具后会自动同步这个源清单。你也可以在界面右侧的 `源订阅` 里点 `刷新源`，不需要重新发软件版本。

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

## Publish A New Version

不用命令行。打开 GitHub 仓库后：

1. 进入 `Actions`。
2. 左侧点 `Release`。
3. 点 `Run workflow`。
4. 在 `version` 里输入新版号，例如 `1.0.1`。
5. 点绿色的 `Run workflow`。

GitHub 会自动创建新版 Release，生成 zip 和 `latest.json`。用户下次启动工具就会检测到更新。

日常只改源列表时，不一定需要发新版；更新 `sources/source-registry.json` 后，工具刷新源就能拿到新源。

## Notes

这个工具保留“可扩展搜索源”的能力，但不会内置未经授权的第三方站点规则。你可以在本地添加自己部署、授权访问或合规使用的聚合接口。
