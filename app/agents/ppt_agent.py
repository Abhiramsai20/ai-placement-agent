import json
import os


class PPTAgent:

    def run(self, state):

        print("\nPPT Agent Running...")

        company = state["company"]

        slides = state.get(
            "slide_content",
            []
        )

        os.makedirs(
            "app/output/slides",
            exist_ok=True
        )

        file_path = (
            f"app/output/slides/"
            f"{company}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                slides,
                f,
                indent=4
            )

        state["slides"] = slides

        print(
            f"Saved {len(slides)} slides"
        )

        print(
            f"Slides JSON saved: {file_path}"
        )

        return state