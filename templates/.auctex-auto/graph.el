(TeX-add-style-hook
 "graph"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "oneside")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "a4paper" "bindingoffset=0.2in" "left=<<params.margin_left>>in" "right=<<params.margin_right>>in" "top=<<params.margin_top>>in" "bottom=<<params.margin_bottom>>in" "footskip=.25in")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "geometry"
    "ifthen"
    "tkz-base"
    "tkz-euclide")
   (TeX-add-symbols
    '("cartesianGraphSet" 8)
    '("cartesianGraph" 6)))
 :latex)

