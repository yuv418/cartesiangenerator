# Cartesian Plane Generator

If you want to generate Cartesian planes to graph things. Install `texlive-most` (Arch) and `poetry install`. Then `poetry run python server.py`.

This is not well designed/implemented and is more just to see how fast I could make this. It uses a Jinja2 template of a LaTeX file to set some parameters. 
The LaTeX file is then compiled to PDF with these parameters, thereby generating Cartesian planes.
