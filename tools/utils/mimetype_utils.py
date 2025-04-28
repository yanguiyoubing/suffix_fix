from enum import StrEnum


class MimeType(StrEnum):
    MD = "text/markdown"
    JSON = "application/json"
    HTML = "text/html"
    TXT = "text/plain"

    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"

    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    CSV = "text/csv"
    XLS = "application/vnd.ms-excel"

    PDF = "application/pdf"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    PPT = "application/vnd.ms-powerpoint"

    JPG = "image/jpeg"
    JPEG = "image/jpeg"
    PNG = "image/png"

    BINARY = "application/octet-stream"
