import os

from app.services.web_search import (
    WebSearchTool
)

from app.services.image_downloader import (
    ImageDownloader
)


class ImageAgent:

    def __init__(self):

        self.search_tool = (
            WebSearchTool()
        )

        self.downloader = (
            ImageDownloader()
        )

    def run(self, state):

        print(
            "\nImage Agent Running..."
        )

        slides = state.get(
            "slide_content",
            []
        )

        os.makedirs(
            "app/output/images",
            exist_ok=True
        )

        image_data = []

        for index, slide in enumerate(
            slides
        ):

            title = slide.get(
                "title",
                ""
            )

            company = state[
                "company"
            ]

            query = (
                f"{company} "
                f"{title}"
            )

            print(
                f"Searching: {query}"
            )

            results = (
                self.search_tool
                .image_search(
                    query,
                    max_results=1
                )
            )

            image_path = None

            if results:

                image_url = (
                    results[0]
                    .get(
                        "image",
                        ""
                    )
                )

                image_path = (
                    f"app/output/images/"
                    f"slide_{index+1}.jpg"
                )

                self.downloader.download(
                    image_url,
                    image_path
                )

            image_data.append(
                {
                    "slide":
                        title,

                    "query":
                        query,

                    "image":
                        image_path
                }
            )

        state["image_data"] = (
            image_data
        )

        print(
            f"Downloaded "
            f"{len(image_data)} images"
        )

        return state