import os
import requests


class ImageDownloader:

    def download(
        self,
        image_url,
        save_path
    ):

        try:

            response = requests.get(
                image_url,
                timeout=10
            )

            if response.status_code == 200:

                with open(
                    save_path,
                    "wb"
                ) as f:

                    f.write(
                        response.content
                    )

                return save_path

        except Exception as e:

            print(
                f"Download Error: {e}"
            )

        return None