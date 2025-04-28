from collections.abc import Generator
from typing import Any, Dict

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File
from tools.utils.mimetype_utils import MimeType

class suffix_fixes(Tool):
    def _invoke(self, tool_parameters: Dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        input_file: File = tool_parameters.get("input_file")
        file_name: str = tool_parameters.get("file_name")

        if not input_file or not isinstance(input_file, File):
            raise ValueError("Not a valid file for input_file")

        input_file_bytes = input_file.blob
        output_style = {
            "md": MimeType.MD,
            "json": MimeType.JSON,
            "html": MimeType.HTML,
            "txt": MimeType.TXT,
            "docx": MimeType.DOCX,
            "doc": MimeType.DOC,
            "xlsx": MimeType.XLSX,
            "csv": MimeType.CSV,
            "xls": MimeType.XLS,
            "pdf": MimeType.PDF,
            "pptx": MimeType.PPTX,
            "ppt": MimeType.PPT,
            "jpg": MimeType.JPG,
            "jpeg": MimeType.JPEG,  # 注意: "jpg" 和 "jpeg" 使用相同的 MIME 类型
            "png": MimeType.PNG
        }

        dot_index = file_name.rfind(".")
        if dot_index == -1 or dot_index == len(file_name) - 1:
            raise ValueError(f"Invalid file name: {file_name}. Expected a file with an extension.")

        suffix = file_name[dot_index + 1:].lower()  # 确保后缀小写以匹配字典键

        try:
            # Check if the suffix is in the dictionary, if not, raise an error or use a default MIME type.
            mime_type = output_style.get(suffix, MimeType.BINARY)  # 使用默认的二进制MIME类型或其他适当的默认值

            result_file_bytes = input_file_bytes
            yield self.create_blob_message(
                blob=result_file_bytes,
                meta={"mime_type": mime_type},
            )
        except Exception as e:
            raise RuntimeError(f"Failed to process file, error: {str(e)}")