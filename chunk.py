import re

def main(input_text: str) -> dict:
    chunk_size_limit = 200

    # 正则表达式匹配章标题（例如“# 第一章”，“# 第二章”）
    chapter_pattern = r'# ?[^#].*[\r\n]+'

    # 正则表达式匹配小节标题（例如“## 第一节”，“## 第二节”）
    section_pattern = r'## ?[\r\n]+'

    # 找到所有的章标题及其位置
    chapters = [(m.start(), m.end()) for m in re.finditer(chapter_pattern, input_text)]

    for start, end in chapters:
        print(input_text[start:end])

    # 初始化变量
    chunks = []

    # 如果没有找到任何章，则返回整个文本作为一个单一的块
    if not chapters:
        return {"chunks": [input_text]}

    # 添加第一个章之前的所有内容作为一个单独的块（如果有）
    if chapters[0][0] > 0:
        chunks.append(input_text[:chapters[0][0]])

    # 遍历所有章，提取每个章的内容
    for i in range(len(chapters)):
        start_index = chapters[i][0]
        end_index = len(input_text) if i == len(chapters) - 1 else chapters[i + 1][0]

        # 提取当前章的内容
        chapter_content = input_text[start_index:end_index]

        current_chapter = ""
        # 检查当前章的内容是否超过限制
        if len(chapter_content)> chunk_size_limit:
            # 如果超过限制，则按节来分割该章
            sections = [(m.start() + start_index, m.end() + start_index) for m in
                        re.finditer(section_pattern, chapter_content)]

            if not sections:
                # 如果没有找到任何小节，则将整章作为一个块
                chunks.append(chapter_content)
            else:
                # 添加第一个小节之前的所有内容作为一个单独的块（如果有）
                if sections[0][0] > start_index:
                    chunks.append(chapter_content[:sections[0][0] - start_index])

                current_chunk = ""
                # 遍历所有小节，提取每个小节的内容
                for j in range(len(sections)):
                    section_start_index = sections[j][0]
                    section_end_index = len(chapter_content) if j == len(sections) - 1 else sections[j + 1][
                                                                                                0] - start_index
                    chunk = chapter_content[section_start_index:section_end_index]

                    if len(current_chunk) + len(chunk) > chunk_size_limit:
                        chunks.append(chunk)
                        current_chunk = chunk
                    else:
                        current_chunk += chunk

                    if j == len(sections) - 1 and len(current_chunk) > 0:
                        chunks.append(current_chunk)
        else:
            if len(chapter_content) + len(current_chapter) <= chunk_size_limit:
                current_chapter += chapter_content
                # 如果未超过限制，则直接添加整章内容
            else:
                chunks.append(chapter_content)
                current_chapter = chapter_content
        if i == len(chapters) - 1 and len(current_chapter) > 0:
            chunks.append(current_chapter)

    # 确保至少有一个块被返回
    if not chunks:
        chunks.append(input_text)

    return {"chunks": chunks}

file_path = "G:\下载\converted.md"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

main(text)

