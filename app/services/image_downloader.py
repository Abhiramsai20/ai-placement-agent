import os
import requests


class ImageDownloader:

    def download(
        self,
        image_url,
        save_path
    ):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        try:

            response = requests.get(
                image_url,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200 and len(response.content) > 500:

                os.makedirs(
                    os.path.dirname(save_path),
                    exist_ok=True
                )

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