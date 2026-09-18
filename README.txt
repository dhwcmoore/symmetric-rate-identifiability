Symmetric rate perturbations of Hodgkin-Huxley gating are observationally equivalent
Duston Moore

Contents
  symmetric_rate_identifiability.tex   manuscript source (elsarticle, JTB preprint format)
  symmetric_rate_identifiability.pdf   compiled manuscript
  CHANGES.md                           point-by-point response to the review, and the earlier reference verification
  fig_equivalence.pdf                  Figure 1
  fig_discrimination.pdf               Figure 2
  model.py                             two-compartment HH model with per-gate rate multipliers
  figures.py                           regenerates both figures and prints every reported number

Reproduction
  python3 figures.py        (requires numpy, scipy, matplotlib)
  pdflatex symmetric_rate_identifiability.tex   (run three times)

Every numerical value quoted in the manuscript is printed by figures.py,
including the gate-selective thermal floor of Section 4.1 and the conductance
divergence table of Section 4.3.

The tex file requires elsarticle.cls, which ships in texlive-publishers. To
compile without it, replace the documentclass line with
\documentclass[11pt]{article} and swap the frontmatter block for \maketitle, as
noted in the comments at the top of the file. Elsevier accepts format-free
initial submissions, so either is acceptable.

The reference list has now been verified against publisher records. See
CHANGES.md for the table of what was checked and what was added.
