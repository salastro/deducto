from deducto.core.proof import ProofState


def export_txt(proof: ProofState, filepath: str):
    lines = []

    # Assumptions section
    lines.append("ASSUMPTIONS:")
    for i, step in enumerate(proof.steps[: len(proof.assumptions)]):
        lines.append(f"{i + 1}: {step.result}")
    lines.append("")
    lines.append(f"GOAL: {proof.goal}")
    lines.append("")

    # Proof steps
    lines.append("PROOF STEPS:")
    for i, step in enumerate(
        proof.steps[len(proof.assumptions) :], start=len(proof.assumptions) + 1
    ):
        premise_refs = [str(j + 1) for j in step.premises]
        rule_name = step.rule.replace("_", " ").capitalize()
        step_index = i - len(proof.assumptions)
        lines.append(
            f"{step_index}. {rule_name} of {', '.join(premise_refs)}"
        )
        lines.append(f"{i}: {step.result}")
        lines.append("")

    lines.append("QED")

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

