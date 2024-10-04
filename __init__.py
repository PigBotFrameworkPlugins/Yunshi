from pbf.utils import MetaData, Utils
from pbf.utils.Config import Config
from pbf.setup import logger
from pbf import config
from pbf.utils.Register import Command, ownerPermission
from pbf.controller.Data import Event
from pbf.controller.Client import Msg
from pbf.statement import Statement

import random
import textwrap
import os
import traceback
import base64
from io import BytesIO
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Utils.installPackage("Pillow==9.3.0")

_root_path = os.path.dirname(__file__)
_TooLucky = ['大吉', '吉你太美']
_TooUnLucky = ['大凶']
_Lucky = ['小吉', '中吉'] + _TooLucky
_UnLucky = ['凶', '小凶'] + _TooUnLucky
_Fortune_List = _Lucky + _UnLucky


class MyConfig(Config):
    originData = {
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
        "tooLucky": _TooLucky,
        "tooUnlucky": _TooUnLucky,
        "lucky": _Lucky,
        "unlucky": _UnLucky,
        "fortuneList": _Fortune_List
    }

config = MyConfig(config.plugins_config.get("yunshi", {}))
todolist = config.get("todoList")
nottodolist = config.get("nottodoList")
TooLucky = config.get("tooLucky")
TooUnLucky = config.get("tooUnlucky")
Lucky = config.get("lucky")
UnLucky = config.get("unlucky")
Fortune_List = config.get("fortuneList")

class ImageStatement(Statement):
    cqtype: str = "image"
    file: str = None

    def __init__(self, file):
        self.file = file

class Api:
    @staticmethod
    def generate(card: str):
        Bold_Font = f"{_root_path}/ttf/SourceHanSansCN-Bold.otf"
        Normal_Font = f'{_root_path}/ttf/SourceHanSansCN-Normal.otf'
        bg_size = (400, 350)
        # 生成背景
        # Generating backgrounds
        img = Image.new('RGB', bg_size, (255, 255, 255))
        draw = ImageDraw.Draw(img)
        # 导入字体
        # Importing Fonts
        Title_Font = ImageFont.truetype(font=Bold_Font, size=20)
        Fortune_Font = ImageFont.truetype(font=Bold_Font, size=60)
        Suitable_To_Do_Font_Bold = ImageFont.truetype(font=Bold_Font, size=16)
        Suitable_To_Do_Font = ImageFont.truetype(font=Normal_Font, size=16)
        Detail_Font = ImageFont.truetype(font=Normal_Font, size=12)
        # 初始化内容
        # Initial content
        title = card + '的运势'
        fortune = '§ ' + random.choice(Fortune_List) + ' §'
        fortune_width = Fortune_Font.getbbox(fortune)[2]
        suitable_to_do, detail = random.choice([['诸事不宜','在家躺一天']] if fortune[2:-2] in TooUnLucky else todolist)
        suitable_to_do, detail = textwrap.fill(suitable_to_do, width=8),textwrap.fill(detail, width=12)

        unsuitable_to_do, detail2 = random.choice([['诸事皆宜', '去做想做的事情吧']] if fortune[2:-2] in TooLucky else nottodolist)
        unsuitable_to_do, detail2 = textwrap.fill(unsuitable_to_do, width=8), textwrap.fill(detail2, width=12)
        while unsuitable_to_do==suitable_to_do:
            unsuitable_to_do,detail2 = random.choice([['诸事皆宜','去做想做的事情吧']] if fortune[2:-2] in TooLucky else nottodolist)
            unsuitable_to_do,detail2 = textwrap.fill(unsuitable_to_do, width=8),textwrap.fill(detail2, width=12)

        suitable_to_do2,detail3 = random.choice([['','']] if fortune[2:-2] in TooUnLucky else todolist)
        suitable_to_do2,detail3 = textwrap.fill(suitable_to_do2, width=8),textwrap.fill(detail3, width=12)
        while suitable_to_do2==suitable_to_do or suitable_to_do2==unsuitable_to_do:
            suitable_to_do2, detail3 = random.choice([['', '']] if fortune[2:-2] in TooUnLucky else todolist)
            suitable_to_do2, detail3 = textwrap.fill(suitable_to_do2, width=8), textwrap.fill(detail3, width=12)

        unsuitable_to_do2,detail4 = random.choice([['','']] if fortune[2:-2] in TooLucky else nottodolist)
        unsuitable_to_do2,detail4 = textwrap.fill(unsuitable_to_do2, width=8),textwrap.fill(detail4, width=12)
        while unsuitable_to_do2==suitable_to_do or unsuitable_to_do2==unsuitable_to_do or unsuitable_to_do2==suitable_to_do2:
            unsuitable_to_do2, detail4 = random.choice([['', '']] if fortune[2:-2] in TooLucky else nottodolist)
            unsuitable_to_do2, detail4 = textwrap.fill(unsuitable_to_do2, width=8), textwrap.fill(detail4, width=12)
        ttd_width = Suitable_To_Do_Font.getbbox(('' if fortune[2:-2] in TooUnLucky else ' ' * 6) + suitable_to_do)[2] if len(suitable_to_do) <= 8 else 152
        tntd_width = Suitable_To_Do_Font.getbbox(('' if fortune[2:-2] in TooLucky else ' ' * 6) + unsuitable_to_do)[2] if len(unsuitable_to_do) <= 8 else 152
        ttd_width2 = Suitable_To_Do_Font.getbbox(' ' * 6 + suitable_to_do2)[2] if len(suitable_to_do2) <= 8 else 152
        tntd_width2 = Suitable_To_Do_Font.getbbox(' ' * 6 + unsuitable_to_do2)[2] if len(unsuitable_to_do2) <= 8 else 152
        detail_width = Detail_Font.getbbox(detail)[2] if len(detail) <= 12 else 144
        detail2_width = Detail_Font.getbbox(detail2)[2] if len(detail2) <= 12 else 144
        detail3_width = Detail_Font.getbbox(detail3)[2] if len(detail3) <= 12 else 144
        detail4_width = Detail_Font.getbbox(detail4)[2] if len(detail4) <= 12 else 144
        name_width = Title_Font.getbbox(title)[2]
        # 绘制
        # Draw
        draw.text(xy=(bg_size[0] / 2 - name_width / 2, 10), text=title, fill='#000000', font=Title_Font)
        draw.text(xy=(bg_size[0] / 2 - fortune_width / 2, 50), text=fortune, fill='#e74c3c' if fortune[2:-2] in Lucky else '#3f3f3f', font=Fortune_Font)
        begin_pos_y=150
        draw.text(xy=(bg_size[0] / 4 - ttd_width / 2, begin_pos_y), text='诸事不宜' if fortune[2:-2] in TooUnLucky else '宜:', fill='#e74c3c', font=Suitable_To_Do_Font_Bold)
        draw.text(xy=(bg_size[0] / 4 - ttd_width / 2, begin_pos_y), text='' if fortune[2:-2] in TooUnLucky else ' ' * 6 + suitable_to_do, fill='#e74c3c', font=Suitable_To_Do_Font)
        draw.text(xy=(bg_size[0] / 4 * 3 - tntd_width / 2, begin_pos_y), text='诸事皆宜' if fortune[2:-2] in TooLucky else '忌:', fill='#000000', font=Suitable_To_Do_Font_Bold)
        draw.text(xy=(bg_size[0] / 4 * 3 - tntd_width / 2, begin_pos_y), text='' if fortune[2:-2] in TooLucky else ' ' * 6 + unsuitable_to_do, fill='#000000', font=Suitable_To_Do_Font)
        len_ttd=len(suitable_to_do.split('\n'))
        begin_pos_y+=25+25*(len_ttd-1)
        draw.text(xy=(bg_size[0] / 4 - detail_width / 2, begin_pos_y), text=detail, fill='#7f7f7f', font=Detail_Font)
        draw.text(xy=(bg_size[0] / 4 * 3 - detail2_width / 2, begin_pos_y), text=detail2, fill='#7f7f7f', font=Detail_Font)

        begin_pos_y=250
        draw.text(xy=(bg_size[0] / 4 - ttd_width2 / 2, begin_pos_y), text='' if fortune[2:-2] in TooUnLucky else '宜:', fill='#e74c3c', font=Suitable_To_Do_Font_Bold)
        draw.text(xy=(bg_size[0] / 4 - ttd_width2 / 2, begin_pos_y), text=' ' * 6 + suitable_to_do2, fill='#e74c3c', font=Suitable_To_Do_Font)
        draw.text(xy=(bg_size[0] / 4 * 3 - tntd_width2 / 2, begin_pos_y), text='' if fortune[2:-2] in TooLucky else '忌:', fill='#000000', font=Suitable_To_Do_Font_Bold)
        draw.text(xy=(bg_size[0] / 4 * 3 - tntd_width2 / 2, begin_pos_y), text=' ' * 6 + unsuitable_to_do2, fill='#000000', font=Suitable_To_Do_Font)
        len_ttd2=len(suitable_to_do2.split('\n'))
        begin_pos_y+=25+25*(len_ttd2-1)
        draw.text(xy=(bg_size[0] / 4 - detail3_width / 2, begin_pos_y), text=detail3, fill='#7f7f7f', font=Detail_Font)
        draw.text(xy=(bg_size[0] / 4 * 3 - detail4_width / 2, begin_pos_y), text=detail4, fill='#7f7f7f', font=Detail_Font)

        return img


meta_data = MetaData(
    name="Yunshi",
    version="0.0.1",
    versionCode=1,
    description="测测你的运势",
    author="XzyStudio",
    license="MIT",
    keywords=["pbf", "plugin", "yunshi"],
    readme="""
# Yunshi
测测你的运势
    """
)


@Command(
        name="运势",
        usage="运势",
        description="测测你的运势",
        permission=ownerPermission
        )
def YunshiGenerate(event: Event):
    # 先遍历一下./tmp/目录下有没有{event.user_id}.jpg，有的话就直接发出去
    for file in os.listdir(f"{_root_path}/tmp"):
        if file == f"{event.user_id}.jpg":
            with open(f"{_root_path}/tmp/{event.user_id}.jpg", "rb") as f:
                img = f.read()
                content = base64.b64encode(img).decode("utf-8")
            break
    else:
        res = Api.generate(event.sender.get("nickname", event.user_id))
        res.save(f"{_root_path}/tmp/{event.user_id}.jpg")
        
        buffered = BytesIO()
        res.save(buffered, format="JPEG")
        content = base64.b64encode(buffered.getvalue())

    # 考虑到有可能OB实现与SDK分离部署，以base64的方式发送图片
    Msg(ImageStatement(f"base64://{content}"), event=event).send()
