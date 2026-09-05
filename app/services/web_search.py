try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None


class WebSearchTool:

    def search(
        self,
        query,
        max_results=5
    ):

        results = []

        if not DDGS:
            return results

        try:

            with DDGS(timeout=5) as ddgs:

                search_results = ddgs.text(
                    query,
                    max_results=max_results
                )

                for r in search_results:

                    results.append(
                        {
                            "title":
                                r.get(
                                    "title",
                                    ""
                                ),

                            "body":
                                r.get(
                                    "body",
                                    ""
                                ),

                            "href":
                                r.get(
                                    "href",
                                    ""
                                )
                        }
                    )

        except Exception as e:

            print(
                f"Search Error: {e}"
            )

        return results

    def image_search(
        self,
        query,
        max_results=5
    ):

        images = []

        if not DDGS:
            return images

        try:

            with DDGS(timeout=5) as ddgs:

                image_results = ddgs.images(
                    query,
                    max_results=max_results
                )

                for img in image_results:

                    images.append(
                        {
                            "title":
                                img.get(
                                    "title",
                                    ""
                                ),

                            "image":
                                img.get(
                                    "image",
                                    ""
                                ),

                            "thumbnail":
                                img.get(
                                    "thumbnail",
                                    ""
                                ),

                            "url":
                                img.get(
                                    "url",
                                    ""
                                )
                        }
                    )

        except Exception as e:

            print(
                f"Image Search Error: {e}"
            )

        return images