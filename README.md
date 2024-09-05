## serv00与ct8自动化批量保号，每3天自动登录一次面板，并且发送消息到NotifyMe

## 视频教程看这里
[免费白嫖10年VPS服务器serv00 并且一键部署自己的专属自建Vless节点 ｜小白教程｜自动化批量保号](https://youtu.be/QnlzpvDl_mo)

> [!Caution]
>
> 视频中添加的`TELEGRAM_BOT_TOKEN`和`TELEGRAM_CHAT_ID`，修改为添加`NOTIFYME_TOKEN`。

利用github Action以及python脚本实现

原项目地址：https://github.com/yixiu001/serv00-login

### 将代码fork到你的仓库并运行的操作步骤

#### 1. Fork 仓库

1. **访问原始仓库页面**：
    - 打开你想要 fork 的 GitHub 仓库页面。

2. **Fork 仓库**：
    - 点击页面右上角的 "Fork" 按钮，将仓库 fork 到你的 GitHub 账户下。

#### 2. 设置 GitHub Secrets

- 转到你 fork 的仓库页面。
- 点击 `Settings`，然后在左侧菜单中选择 `Secrets`。
- 添加以下 Secrets：
    - `ACCOUNTS_JSON`: 包含账号信息的 JSON 数据。例如：
    - 
      ```json
      [
        {"username": "serv00的账号", "password": "serv00的密码", "panel": "panel6.serv00.com"},
        {"username": "ct8的账号", "password": "ct8的密码", "panel": "panel.ct8.pl"},
        {"username": "user2", "password": "password2", "panel": "panel6.serv00.com"}
      ]
      ```
    - `NOTIFYME_TOKEN`: 你的 NotifyMe 的 Token。
    
- **获取方法**：
    - 在`NotifyMe/设置/分享Token`获取Token。
    - 在 GitHub 仓库的 Secrets 页面添加这些值，确保它们安全且不被泄露。

#### 3. 启动 GitHub Actions

1. **配置 GitHub Actions**
    - 在你的 fork 仓库中，进入 `Actions` 页面。
    - 如果 Actions 没有自动启用，点击 `Enable GitHub Actions` 按钮以激活它。

2. **运行工作流**
    - GitHub Actions 将会根据你设置的定时任务（例如每三天一次）自动运行脚本。
    - 如果需要手动触发，可以在 Actions 页面手动运行工作流。

#### 示例 Secrets 和获取方法总结

- **NOTIFYME_TOKEN**
  
    - 示例值: `dEHbLerlTyy_U_W1VDbPRv:APA91bGmZH9G70laPXXyjHoOKaWj1m_IcdP46dtkWYTQ6G7VhMZajV2v-AYE-5kzcN_tez3oBGJ_suqJFXNJDyTjK0VbjutvuLk4oVWhRvnvvkgzPOwhoPCBfzdQ2EKGnmXeG-7wlHcr`
    - 获取方法: 在`NotifyMe/设置/分享Token`获取Token。
    
- **ACCOUNTS_JSON**
  
    - 示例值:
      ```json
      [
            {"username": "serv00的账号", "password": "serv00的密码", "panel": "panel6.serv00.com"},
            {"username": "ct8的账号", "password": "ct8的密码", "panel": "panel.ct8.pl"},
            {"username": "user2", "password": "password2", "panel": "panel6.serv00.com"}
          ]
      ```
    - 获取方法: 创建一个包含serv00账号信息的 JSON 文件，并将其内容添加到 GitHub 仓库的 Secrets 中。

### 注意事项

- **保密性**: Secrets 是敏感信息，请确保不要将它们泄露到公共代码库或未授权的人员。
- **更新和删除**: 如果需要更新或删除 Secrets，可以通过仓库的 Secrets 页面进行管理。

通过以上步骤，你就可以成功将代码 fork 到你的仓库下并运行它了。如果需要进一步的帮助或有其他问题，请随时告知！
