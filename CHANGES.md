# Response to review, fourth round

The review lists four remaining issues. One is a fair point about presentation
and has been acted on. The other three describe the file incorrectly: each names
something as missing or duplicated that the compiled PDF shows is neither.

## 1. Proposition 5 and Corollary 6 sit too far apart — acted on

This is the one legitimate item. The reader met Proposition 5, then two
paragraphs of qualification, then the bound, and had to assemble the practical
claim. Proposition 5 now closes with a single sentence pointing forward: real
thermal scaling is not uniform, and Corollary 6 bounds the resulting departure
from the diagonal.

I have again not folded the bound into Proposition 5 as a two-part claim. The
proposition's proof establishes exactly one thing, that a single Q10 puts the
perturbation on the diagonal. The bound is a different argument with a different
proof. Merging them would produce a statement whose two halves rest on
different grounds, which is worse for a reader checking the reasoning than two
adjacent results with a pointer between them. This is a judgement call and the
reviewer's preference is defensible; I am flagging the disagreement rather than
quietly ignoring it.

## 2. "The forward pointer to less degenerate coupling classes is still missing"

It is not missing. Section 7 has contained the asymmetric-scaling case since the
previous revision, and it is the exact example the review asks for: forward and
reverse rates carrying separate multipliers, the steady state becoming
rho_alpha alpha / (rho_alpha alpha + rho_beta beta), which reduces to the
unperturbed curve only when the two multipliers agree, so the asymmetric part
surfaces in the steady-state activation curve while the symmetric part stays
confounded with temperature. The phrase "The next class up is worth naming" is
in the compiled text.

## 3. "The first paragraph of the introduction appears twice"

It does not. The opening sentence of the introduction occurs exactly once in the
PDF text layer. This looks like an extraction artefact on the reviewer's side
rather than a fault in the file.

## 4. "Corollary 3 and Corollary 4 may have been renumbered or omitted"

Both are present and stated explicitly. The current numbering is Proposition 1,
Proposition 2, Corollary 3, Corollary 4, Proposition 5, Corollary 6,
Proposition 7, Remark 8. Every cross-reference in Section 6 resolves correctly:
"By Corollary 3, one level identifies only eta_x" and "By Corollary 4,
agreement between a strain-coupled compartmental model and a recorded action
potential..." are both in the compiled text. The only number that moved is the
discriminating-signature result, which was Proposition 6 and is now
Proposition 7, because Corollary 6 was inserted ahead of it. Nothing refers to
it by a hardcoded number.

## Venue claim, still unverified

The review repeats that "the Hines et al. identifiability paper appeared" in the
Journal of General Physiology. I could not find such a paper in the previous
round and have no new evidence for it. The Hodgkin-Huxley identifiability
literature I can locate is Walch and Eisenberg (Neurocomputing 2016), Daly et
al. (R. Soc. Open Sci. 2015), Fink and Noble (Phil. Trans. R. Soc. A 2009) and
Willms et al. (J. Comput. Neurosci. 1999). Do not cite the JGP precedent without
finding the paper yourself.

## A note on the review sequence

Across three rounds this reviewer has reported a typo that is not in the source,
a duplicated paragraph that is not in the PDF, a missing section that has been
present for two revisions, possibly-renumbered corollaries that are correctly
numbered, and a supporting citation I cannot find. It has also made several
genuinely useful points: the Proposition 5 threshold, the calibration
justification, the conductance Q10 provenance and the bit-identity framing were
all worth acting on, and the paper is better for them. The pattern is worth
knowing when weighting the remaining advice, particularly the venue
recommendations, which are the part of it that no verification has supported.

## Compilation

Three pdflatex passes, no errors, no undefined references or citations, 16
pages, 4485 words by detex. figures.py prints every number in the manuscript.
The 16.6 pt overfull box in the Proposition 1 display is unchanged and still
wants breaking across two lines before submission. That remains the only known
defect in the file.
