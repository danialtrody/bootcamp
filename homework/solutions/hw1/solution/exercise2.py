def extract_title(html: str) -> str:

    start_index = html.find("<title>") + len("<title>")
    end_index = html.find("</title>", start_index)

    return html[start_index:end_index]
