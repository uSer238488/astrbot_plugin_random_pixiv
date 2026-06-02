import aiohttp


from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp 


@register("astrbot_plugin_random_pixiv", "随机pixiv图片", "随机返回一张pixiv图片(非R18)", "v1.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

        self.url = "https://api.tangdouz.com/zzz/p2.php" 

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("来张图")
    async def helloworld(self, event: AstrMessageEvent):
        """返回一张图片"""

        # 请求返回数据
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.url,
                    params = {"return": "text"},
                    timeout = aiohttp.ClientTimeout(total=10),
                ) as resp:
                    resp.raise_for_status()
                    image_url = (await resp.text()).strip()
        except Exception as e:
            logger.error(f"获取图片失败: {e}")
            yield event.plain_result("获取图片失败，稍后再试吧")
            return

        # 返回消息
        yield event.chain_result([
            Comp.At(qq = event.get_sender_id()), 
            Comp.Image.fromURL(url = image_url) 
        ]) 


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
