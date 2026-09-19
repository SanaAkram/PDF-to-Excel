# PDF-to-Excel

A prototype for turning a **fillable/structured PDF form into spreadsheet data**. The worked example is an insurance **"4-Point inspection" template**: the goal is to pull the insured's details, the property address, the year built, the inspection date and the ticked checkboxes out of the PDF and write them to CSV / Excel-ready rows.

## What it does

`4pt.py` runs three extractions on `inputs/4pt Template.pdf`:

1. **Text → fields → CSV** — with `pdfplumber` it reads every page's text, splits lines into `label: value` pairs and looks for the key form fields (*Insured/Applicant Name*, *Application/Policy #*, *Address*, *Actual Year Built*, *Date Inspected*). The address is normalised by `format_address()` and the rows are written to `outputs/output.csv`.
2. **Checkboxes** — detects ticked (`✓`) and unticked (`✗`) options, starting at the *Dwelling* section of the form (`get_checkbox()`).
3. **Embedded images** — with PyMuPDF it saves every image on every page to `images_<file>/page_<n>_image_<i>.png` (the repo contains the resulting `images_4pt/` folder).

`box.py` is a companion experiment that uses `pdfminer.six`'s `XMLConverter` to export the **text layout with bounding boxes** as `output.xml`, which is what you need when a field must be located by position (for example, checkboxes).

## Repository contents

| Path | Purpose |
|---|---|
| `4pt.py` | Main extraction script (text → CSV, checkbox detection, image export) |
| `box.py` | PDF text + layout (bounding boxes) → `output.xml` via pdfminer |
| `pdfkit_example.py` | Small `pdfkit` example (HTML → PDF) used while testing |
| `inputs/` | The sample PDF/DOCX template being parsed |
| `outputs/`, `output.xml`, `pdfXML.html` | Generated results |
| `images_4pt/`, `output_images/`, `page_image.png` | Extracted / rendered page images |
| `Template.pdf` | A copy of the template PDF |
| `requirements.txt` | Pinned dependencies |

## How it works

```
inputs/4pt Template.pdf
   ├── pdfplumber ── page text ── label:value parsing ── format_address() ─► outputs/output.csv
   ├── checkbox detection (✓ / ✗ symbols) ────────────────────────────────►  checked / unchecked lists
   ├── PyMuPDF (fitz) ── embedded images ─────────────────────────────────►  images_4pt/*.png
   └── pdfminer XMLConverter (box.py) ── text + bounding boxes ───────────►  output.xml
```

The requirements also include `tabula-py` and `camelot-py`, which are the table-extraction tools to reach for when a form contains real tables rather than label/value lines.

## Stack

- Python 3.9+
- `pdfplumber`, `PyMuPDF` (`fitz`), `pdfminer.six`, `PyPDF2`/`pypdf`, `tabula-py` (needs Java), `camelot-py`
- `pandas`, `openpyxl` (for Excel output), `opencv-python`, `Pillow`

## Install

```bash
git clone https://github.com/SanaAkram/PDF-to-Excel.git
cd PDF-to-Excel

python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r requirements.txt
pip install pdfplumber PyPDF2 opencv-python pdfquery   # imported by 4pt.py
```

`tabula-py` needs a Java runtime (JRE 8+) on your `PATH`.

## Run

```bash
python 4pt.py      # → outputs/output.csv and images_4pt/*.png
python box.py      # → output.xml (text with layout coordinates)
```

To parse a different PDF, change `first_temp_file` at the top of `4pt.py` (and `pdf_file` in `box.py`).

## Notes

- This is a work-in-progress prototype tuned to one template; field labels are matched by text, so another form needs its own label handling.
- To get an Excel file rather than CSV, load the CSV with `pandas.read_csv(...).to_excel("output.xlsx", index=False)`.
