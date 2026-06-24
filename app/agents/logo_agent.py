import os

from app.services.web_search import (
    WebSearchTool
)

from app.services.image_downloader import (
    ImageDownloader
)


class LogoAgent:

    def __init__(self):

        self.search_tool = (
            WebSearchTool()
        )

        self.downloader = (
            ImageDownloader()
        )

    def run(self, state):

        print(
            "\nLogo Agent Running..."
        )

        company = state["company"]

        os.makedirs(
            "app/output/logos",
            exist_ok=True
        )

        query = (
            f"{company} company logo"
        )

        results = (
            self.search_tool
            .image_search(
                query,
                max_results=1
            )
        )

        logo_path = None

        if results:

            logo_url = (
                results[0]
                .get(
                    "image",
                    ""
                )
            )

            logo_path = (
                f"app/output/logos/"
                f"{company}.png"
            )

            self.downloader.download(
                logo_url,
                logo_path
            )

        state["logo_path"] = (
            logo_path
        )

        print(
            f"Logo Saved: {logo_path}"
        )

        return state