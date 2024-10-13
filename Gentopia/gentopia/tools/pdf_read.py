from typing import AnyStr, Any, Optional, Type
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool, BaseModel, Field

class PDFReadFromURLArgs(BaseModel):
    url: str = Field(..., description="The URL of the PDF to download and read.")

class PDFRead(BaseTool):
    description = ("Downloads a PDF from a given URL and extracts the text."
                   "Input should be the URL of the PDF.")
    name = "read_pdf"
    args_schema: Optional[Type[BaseModel]] = PDFReadFromURLArgs
    def _run(self, url: AnyStr) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()  
            data_of_pdf = BytesIO(response.content)
            r = PdfReader(data_of_pdf)
            text = ""
            for page in r.pages:
                text += page.extract_text()
            return text
        except requests.exceptions.RequestException as e:
            return f"Failed to download PDF: {str(e)}"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    url_in = input("Please provide the URL of the PDF: ")
    p_read = PDFReadFromURL()
    res = p_reader._run(url_in)
    print(res)
