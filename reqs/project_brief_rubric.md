# COMP30770 — Programming for Big Data

## Group Project Brief (2025/26 Spring)

---

## 📋 Important Notes

- Only **1 PDF file per group** is required for each submission. Multiple submissions are allowed, but only **the most recent one** will be kept.
- The report should be in **single-column, A4 size**, with a **minimum font size of 8**.
- Suggested section lengths are marked below. Less than 1 page deviation from the suggested length is acceptable.
- Each section is evaluated on **technical clarity and soundness**.
- **6 marks** (not covered in the report) account for your **group conduct mark** for lab session engagement with TA/demonstrators. If all group members are absent with no valid explanation, those marks will be lost.

---

## 📄 Report Template

**Project Title:** `[No more than 20 words]`

**Group Members:** `Student1 (Name, UCD ID); Student2 (Name, UCD ID); … Student6 (Name, UCD ID)`

> Please don't miss anyone in your group — the same grade is given to all members by default.

**Code Link:** Provide a publicly accessible (or at least within UCD) link (e.g., GitHub, GitLab, Google Drive) to all code relevant to this project. This link must be valid before the end of **May 2026**.

---

## Section 1 — Introduction

**Length:** 1 page | **Marks:** 4

- **Dataset description** (2–3 sentences) — justify how it relates to big data:
  - **Volume:** Not just file size (e.g., XX GB/TB). Present your hardware/software specs and cite execution times from key steps in Section 2.
  - **Variety:** Datasets don't have to be structured/unstructured/semi-structured — justify that the two or more datasets have different structures or different impacts toward achieving your "value".
- **Objective** (1 sentence) — explain the overall project goal. 1–2 additional sentences may be used to explain the **"value"** of your big data project.

---

## Section 2 — Traditional Solution

**Length:** 2 pages | **Marks:** 10

Before building the big data pipeline, build a **prototype** on a smaller version of the dataset to validate processing logic and establish a performance baseline. This prototype must use **no parallelism** and can use any high-level language (Shell, SQL, Python, Java, C++, etc.).

Decompose your overall objective into **3–6 small steps**:

> Each step should translate directly to one or a few Shell/SQL statements or small code snippets.

For each step, include:

- A brief description of the step
- Key code (not all code) — single-threaded solution in your chosen language
- Execution results, execution time, and memory requirements

---

## Section 3 — MapReduce Optimisation

**Length:** 2 pages | **Marks:** 10

Identify **1–2 of the most time-consuming steps** from Section 2 that can be optimised using MapReduce.

> You may use either **Hadoop MapReduce** or **Spark MapReduce (Spark Core API only — NOT Spark SQL or DataFrames)**.

For each optimised step, include:

1. **Justification** — why can this step benefit from MapReduce? State your expectations (e.g., "expect 2× speedup").
2. **MapReduce solution** — define your map and reduce functions clearly.
3. **Results** — present the actual MapReduce execution results.
4. **Analysis** — explain why the results matched or deviated from your expectations.

---

## 🏆 Grading Rubric

### Section 1 — Introduction (4 marks)


| Grade                      | Marks     | Criteria                                                                                                                                                                                                                                                                                                                                          |
| -------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Good / Excellent**       | 4.0 – 3.0 | **Technical:** Clearly defines dataset "Volume" relative to hardware specs (not just file size) and "Variety" regarding structure/impact. Objective is non-trivial and "value" is explicitly justified. Code link is accessible and valid. **Clarity:** Concise (2–3 sentences for dataset, 1 for objective). Professional writing, no ambiguity. |
| **Satisfactory / Average** | 2.5 – 2.0 | **Technical:** Dataset is described but lacks specific justification for why it counts as "Big Data" (e.g., missing hardware context). Objective is understandable but generic. Code link is present. **Clarity:** Explanations are present but may be wordy or slightly vague.                                                                   |
| **Fail / Poor**            | 1.5 – 0.0 | **Technical:** Missing crucial details (e.g., no code link or invalid link). Dataset is trivial or clearly not "Big Data." No clear objective. **Clarity:** Poorly written, confusing structure, or significantly exceeds page limits.                                                                                                            |


---

### Section 2 — Traditional Solution (10 marks)


| Grade                      | Marks      | Criteria                                                                                                                                                                                                                                                                                                             |
| -------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Good / Excellent**       | 10.0 – 7.0 | **Technical:** Problem logically decomposed into 3–6 distinct steps. Prototype uses a non-parallel language successfully. Execution time and memory baselines measured and recorded accurately. **Clarity:** Code snippets are relevant and readable. Logic flow is easy to follow. Steps are clearly distinguished. |
| **Satisfactory / Average** | 6.5 – 4.0  | **Technical:** Decomposition exists but steps are overlapping or ill-defined. Prototype works, but baseline performance metrics are estimated or missing detail. **Clarity:** Code pasted without sufficient context. Narrative flow between steps is disjointed.                                                    |
| **Fail / Poor**            | 3.5 – 0.0  | **Technical:** Fails to build a prototype, or uses parallel tools (e.g., Spark) prematurely in this section. Code is broken or logic is fundamentally flawed. **Clarity:** Missing code evidence. Steps not described. Impossible to verify the baseline.                                                            |


---

### Section 3 — MapReduce Optimisation (10 marks)


| Grade                      | Marks      | Criteria                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Good / Excellent**       | 10.0 – 7.0 | **Technical:** Correctly identifies the bottleneck step from Section 2. Implementation strictly uses Hadoop MR or Spark Core (RDDs). Logic correctly translated to K-V pairs / Map / Reduce. Results analysed with deep insight into why performance matched or deviated from expectations. **Clarity:** Clear definition of Map vs. Reduce functions. Compelling "Before vs. After" performance comparison. |
| **Satisfactory / Average** | 6.5 – 4.0  | **Technical:** Optimises a step that wasn't the bottleneck. Uses correct API but with inefficient logic (e.g., poor key selection). Comparison is superficial (e.g., "It was faster" with no explanation). **Clarity:** Map/Reduce logic is hard to decipher. Expectations are missing or unrealistic.                                                                                                       |
| **Fail / Poor**            | 3.5 – 0.0  | **Technical:** ⚠️ **Major Violation:** Uses Spark SQL / DataFrames instead of Core API. Code does not run or produces different results from Section 2. No optimisation achieved. **Clarity:** No code presented. No analysis of results.                                                                                                                                                                    |


---

### Lab Conduct (6 marks)

Marks awarded for group engagement with TA/demonstrators during lab sessions. Unjustified absence by all group members will result in loss of these marks.

---

### Total: 30 marks

