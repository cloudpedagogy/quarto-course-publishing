# Running the System

This guide covers the three main commands used to run the Quarto Course Publishing System: `build`, `import-word`, and `render`.

## Before you start

Before running the system, you should already have:
- installed Python, R, Pandoc, and Quarto
- created and activated a virtual environment
- installed Python requirements with `pip install -r requirements.txt`
- opened your terminal or command prompt in the project root folder

*(For detailed setup steps, see [PREREQUISITES.md](PREREQUISITES.md))*

## Demo configuration

The demo uses the configuration file:
`config/outbreak_ve_demo.yml`

## Mac / Linux commands

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/outbreak_ve_demo.yml
PYTHONPATH=src python3 -m course_generator.cli import-word config/outbreak_ve_demo.yml
PYTHONPATH=src python3 -m course_generator.cli render config/outbreak_ve_demo.yml
```

## Windows Command Prompt commands

```cmd
set PYTHONPATH=src && python -m course_generator.cli build config/outbreak_ve_demo.yml
set PYTHONPATH=src && python -m course_generator.cli import-word config/outbreak_ve_demo.yml
set PYTHONPATH=src && python -m course_generator.cli render config/outbreak_ve_demo.yml
```

## What each command does

- **build**: creates the course structure and QMD files
- **import-word**: converts DOCX content into Markdown and inserts it into QMD files
- **render**: uses Quarto to generate the final HTML output

## Viewing the output

The rendered course is available at:
`output/outbreak_ve_demo/index.html`

### Optional local server preview

You can serve the output locally with Python:

```bash
python3 -m http.server 8000 --directory output/outbreak_ve_demo
```

Then open:
[http://localhost:8000](http://localhost:8000)

## Common issues

- **"Target QMD not found"** usually means build did not run successfully or output folders changed
- **R render errors** may mean R/knitr is missing or an R Code block is not closed with `END R Code`
- If port 8000 is already in use, try port 8001
- Re-run `import-word` after changing Word documents
