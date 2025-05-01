from pylatex import Command, Document, Section
from pylatex.utils import NoEscape, bold

from deducto.core.proof import ProofState


def format_expr(expr):
    return (
        str(expr)
        .replace("¬", r"\lnot ")
        .replace("∨", r"\lor ")
        .replace("∧", r"\land ")
        .replace("→", r"\rightarrow")
        .replace("↔", r"\leftrightarrow ")
        # .replace("∀", r"\forall ")
        # .replace("∃", r"\exists ")
        # .replace("⊥", r"\bot ")
        # .replace("⊤", r"\top ")
        .replace("(", r"\left(")
        .replace(")", r"\right)")
        .replace("𝗧", r"\mathbf{T}")
        .replace("𝗙", r"\mathbf{F}")
    )


def generate_structured_latex_from_proofstate(proof: ProofState, filepath: str):
    doc = Document()

    # Assumptions section
    with doc.create(Section("Assumptions")):
        for i, step in enumerate(proof.steps[: len(proof.assumptions)]):
            expr = format_expr(step.result)
            doc.append(NoEscape(r"\begin{equation}"))
            doc.append(NoEscape(expr))
            doc.append(NoEscape(rf"\label{{eq:{i + 1}}}"))
            doc.append(NoEscape(r"\end{equation}"))
        doc.append(NoEscape(rf"\textbf{{Goal}}: ${format_expr(proof.goal)}$"))

    # Proof Steps
    with doc.create(Section("Proof Steps")):
        for i, step in enumerate(
            proof.steps[len(proof.assumptions) :], start=len(proof.assumptions) + 1
        ):
            premise_refs = [rf"\ref{{eq:{j + 1}}}" for j in step.premises]
            doc.append(
                NoEscape(
                    rf"\textbf{i-len(proof.assumptions)}. {step.rule.replace('_', ' ').capitalize()} of {', '.join(premise_refs)}"
                )
            )
            doc.append(NoEscape(r"\begin{equation}"))
            doc.append(NoEscape(format_expr(step.result)))
            doc.append(NoEscape(rf"\label{{eq:{i}}}"))
            doc.append(NoEscape(r"\end{equation}"))
        doc.append(NoEscape(r"\hfill"))
        doc.append(bold("QED"))

    doc.generate_tex(filepath)
    doc.generate_pdf(filepath, clean_tex=True)
