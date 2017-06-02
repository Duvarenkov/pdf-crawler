from PyPDF2 import PdfFileReader

KEY = '/Annots'
ANK = '/A'
URI = '/URI'


def get_links_from_pdf(file_obj):
    """
    Function that receives file-like object, parses it as PDF
    and returns a list of external links in this PDF.
    """

    pdf = PdfFileReader(file_obj)
    pgs = pdf.getNumPages()

    links = []

    for pg in range(pgs):

        page = pdf.getPage(pg)
        annotations = page.get(KEY)

        if annotations:
            for annotation in annotations.getObject():
                link = annotation.getObject()[ANK].get(URI)
                if link:
                    links.append(link)

    return links
