import aiohttp

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp


IMAGE_HEADERS = {
    "Referer": "https://www.pixiv.net/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


@register("astrbot_plugin_random_pixiv", "随机pixiv图片", "随机返回一张pixiv图片(非R18)", "v1.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.url = "https://api.tangdouz.com/zzz/p2.php"

    @filter.command("来张图")
    async def helloworld(self, event: AstrMessageEvent):
        try:
            async with aiohttp.ClientSession() as session:
                # 1. 取图片 URL
                async with session.get(
                    self.url,
                    params={"return": "text"},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    resp.raise_for_status()
                    image_url = (await resp.text()).strip()

                # 2. 下载图片(带 Referer 绕过防盗链)
                async with session.get(
                    image_url,
                    headers=IMAGE_HEADERS,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as img_resp:
                    img_resp.raise_for_status()
                    image_bytes = await img_resp.read()
        except Exception as e:
            logger.error(f"获取图片失败: {e}")
            yield event.plain_result("获取图片失败,稍后再试吧")
            return

        chain = [
            Comp.At(qq=event.get_sender_id()),
            Comp.Image.fromBytes(image_bytes),
        ]
        yield event.chain_result(chain)
