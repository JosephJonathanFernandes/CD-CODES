# Viva Questions & Model Answers — Predictive Parser Experiment

Below are exam-style questions and concise model answers to help you prepare for a viva on the predictive parser experiment (left-recursion removal, left-factoring, FIRST/FOLLOW, LL(1) table-driven parsing).

---

## Basics & definitions

1. **Q:** What is an LL(1) grammar?

   **A:** An LL(1) grammar is parsed top-down, left-to-right, producing a leftmost derivation with 1 token lookahead. For every nonterminal A and terminal a, the parsing table T[A,a] must contain at most one production. FIRST/FOLLOW sets are used to populate the table.

2. **Q:** What do FIRST(X) and FOLLOW(A) mean?

   **A:** FIRST(X) is the set of terminals that can appear at the beginning of strings derived from X (including ε if X can derive the empty string). FOLLOW(A) is the set of terminals that can appear immediately to the right of A in some sentential form; the end marker `$` belongs to FOLLOW(start-symbol).

3. **Q:** Why are FIRST and FOLLOW needed for LL(1) parsing?

   **A:** FIRST tells which terminals begin productions (used to populate table entries). When a production can derive ε, its placement in the table depends on FOLLOW(A) so the parser knows to apply the ε-production when the next input token is in FOLLOW(A).

---

## Left recursion and left factoring

4. **Q:** What is left recursion? Give direct and indirect forms.

   **A:** Direct left recursion: A → A α. Indirect: A → B α and B ⇒* A β (A derives itself via other nonterminals). Both prevent simple top-down parsing and must be eliminated for LL(1).

5. **Q:** How do you remove direct left recursion A → A α | β?

   **A:** Introduce A' and rewrite:
   - A → β A'
   - A' → α A' | ε
   This converts left recursion to right recursion.

6. **Q:** How is indirect left recursion removed?

   **A:** Order nonterminals A1..An. For i=1..n replace productions Ai→Aj γ where j<i by expanding Aj's productions (Ai→β γ for each Aj→β). Then remove direct left recursion for Ai. Repeat.

7. **Q:** What is left factoring and when is it used?

   **A:** Left factoring extracts common prefixes when alternatives share the same start symbols. Example: A→a B | a C becomes A→a A' ; A'→B | C. It is used when single-token lookahead cannot distinguish alternatives.

---

## Parsing-table construction and conflicts

8. **Q:** How do you construct the LL(1) parsing table T[A,a]?

   **A:** For each production A→α:
   - For each terminal a in FIRST(α) \ {ε}, set T[A,a] = α.
   - If ε ∈ FIRST(α), then for each b in FOLLOW(A) set T[A,b] = α.
   If multiple productions map to the same cell, it's a conflict (not LL(1)).

9. **Q:** What causes table conflicts? Example.

   **A:** Overlap in FIRST sets between alternatives, or FIRST/FOLLOW overlaps when ε-productions exist. Example: A→a α | a β yields both alternatives with `a` in FIRST, so T[A,a] is ambiguous.

10. **Q:** In the conflict message `existing -> S ⇒ A a, new -> S ⇒ b` what does "new" mean?

   **A:** "New" is the production currently being inserted into the table cell while building the table; "existing" is the production that already occupies that cell. The message shows which production first filled the cell and which one attempted to overwrite it.

---

## Parser trace & behavior

11. **Q:** Explain the columns in the parse trace: Buffer | Stack | Action.

   **A:** Buffer shows remaining input tokens (with `$` end marker). Stack shows parser stack with top on the left. Action indicates table lookups (T[A,a] = A ⇒ ...), matched terminals, or errors/Accept. After expanding a nonterminal the updated stack state is printed so you can see before/after.

12. **Q:** How are ε-productions handled during parsing?

   **A:** If a table entry yields ε, the parser does not push any symbols for that production (i.e., it effectively pops the nonterminal and proceeds). The ε-production is placed in table cells corresponding to FOLLOW(A).

13. **Q:** What happens if a table cell is empty during parse?

   **A:** The parser reports an error (no rule) and the input is rejected.

---

## Implementation-specific and project files

14. **Q:** Which file contains the main parser and grammar transformations?

   **A:** `expt6.py`.

15. **Q:** How should grammar files be formatted for this program?

   **A:** Plain UTF-8 text. Use `->` in the file for productions. Optional `Start: S` and `Input: tokens` allowed. Symbols should be space-separated. Use `ε` or `eps` for epsilon.

16. **Q:** How are productions printed in output?

   **A:** The program prints productions using a display-only arrow `PROD_ARROW` (default `⇒`) — this is only for output. Grammar files still use `->`.

17. **Q:** Where are tests and sample grammars stored?

   **A:** `tests/grammars/` and the runner is `tests/run_tests.py`; outputs are stored in `tests/results/`.

18. **Q:** How does the program print ε correctly on Windows consoles?

   **A:** The code attempts to reconfigure stdout/stderr to UTF-8 and the test runner sets `PYTHONIOENCODING=utf-8`, ensuring `ε` prints correctly.

---

## Deeper reasoning and debugging

19. **Q:** The grammar `S → A a | b`, `A → S d | c` produced table conflicts. Why?

   **A:** After expanding indirect recursion and removing direct recursion, FIRST/FOLLOW sets overlap for some alternatives. For example `b` may appear in FIRST of both S→A a (after expansion) and S→b, so T[S,b] is ambiguous. Also ε/FOLLOW overlap can cause conflicts when ε-productions are present.

20. **Q:** How can you resolve table conflicts in practice?

   **A:** Options: left-factor the grammar; rewrite productions to remove ambiguity; use more lookahead (LL(k)); or switch to a different parsing strategy (LR) if grammar requires more power.

21. **Q:** Complexity: how costly are FIRST/FOLLOW and table construction?

   **A:** Iterative fixpoint computations for FIRST/FOLLOW are typically linear to modest polynomial in grammar size and converge quickly for classroom grammars. Table construction is proportional to the number of productions times number of terminals in the worst case.

---

## Live viva prompts (practice)

22. **Q (live):** Left-factor `A → a B | a C | d`.

    **A:** `A → a A' | d` ; `A' → B | C`.

23. **Q (live):** Remove left recursion for `A → A a | b`.

    **A:** `A → b A'` ; `A' → a A' | ε`.

24. **Q (debug):** A trace shows `T[A'][a] = A' ⇒ a d A'` then later `T[A'][a] = A' ⇒ ε` attempted — what does that suggest?

    **A:** The ε-production for A' is being placed into table cells for FOLLOW(A'), and `a ∈ FOLLOW(A')`, so the ε entry tries to fill T[A'][a] and conflicts with the a-starting alternative — indicating non-LL(1).

25. **Q (meta):** Limitations of this tool and possible improvements?

    **A:** The tool supports LL(1) style parsing only; tokenizer and grammar format are simple. Improvements: CLI flags for verbosity/arrow choice, automatic factoring, exportable HTML/Markdown reports, support for LL(k) or LR parsing, and more robust tokenization.

---

## Tips for viva answers

- Explain steps succinctly; when asked for an algorithm sketch its stepwise procedure and a short example.
- When diagnosing a conflict, point to the FIRST/FOLLOW overlap causing it and propose the smallest rewrite to fix it if possible.
- Mention filenames (`expt6.py`, `tests/run_tests.py`, `tests/grammars/`) when asked where logic lives.

