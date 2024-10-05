# Yunshi
测测你的运势

# 特性
当发送`运势`指令时，为用户生成仿洛谷的运势图片，并发送。

插件也提供Api对外开放，您可以通过
```python
from pbf.setup import pluginsManager
YunshiApi = pluginsManager.require("yunshi")
img = YunshiApi.generate("User NickName")
```
来生成。

# 配置
原始配置如下
```python
config.plugins_config["yunshi"] = {
    "todoList": [
        ['刷B站','承包一天笑点'],
        ['在QQ群聊天','遇见好朋友'],
        ['被撅','哼哼哼啊啊啊啊啊'],
        ['写作业','蒙的全对'],
        ['唱跳RAP篮球','只因你太美'],
        ['打游戏','杀疯了'],
        ['摸鱼','摸鱼不被发现']
    ],
    "nottodoList": [
        ['刷B站','视频加载不出来'],
        ['在QQ群聊天','被小鬼气死'],
        ['被撅','休息一天~'],
        ['写作业','全错了'],
        ['唱跳RAP篮球','被ikun人参公鸡'],
        ['打游戏','送人头'],
        ['摸鱼','摸鱼被发现']
    ],
    "tooLucky": ['大吉', '吉你太美'],
    "tooUnlucky": ['大凶'],
    "lucky": ['小吉', '中吉', '大吉', '吉你太美'],
    "unlucky": ['凶', '小凶', '大凶'],
    "fortuneList": ['小吉', '中吉', '大吉', '吉你太美', '凶', '小凶', '大凶']
}
```
本插件使用`pbf.utils.Config.Config`来管理配置，您可以自由传参。
