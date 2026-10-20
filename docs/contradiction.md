# Contradiction

## Overview & Classification

Contradiction can come from different reasons. We classify contradictions into two main categories:

1. **Structural Logic**
* Strict Contradiction
* Contrary / Conditional Contradiction
* Quantification Contradiction


2. **Content & Context**
* Lexical
* Temporal
* Pragmatic



---

## Structural Logic

### Strict Contradiction

Two sentences are contradictory if they can never both be true, and never both be false at the same time. If one is true, the other must be false.

**Example 1:**

```text
- Today is Tuesday.
- Today is not Tuesday.

```

### Contrary Contradiction

Two sentences cannot both be true, but they can both be false depending on missing information or context.

**Example 2:**

```text
- Doc A: "The medication causes drowsiness."
- Doc B: "The medication does not cause drowsiness."

```

> **Missing information:** Doc A might be true only when taken with alcohol, while Doc B is true when taken alone. Without the condition, they appear to clash.

**Example 3:**

```text
- Doc A: "The car is painted black."
- Doc B: "The car is painted white."

```

> **Missing information:** The car cannot be painted solid black and white at the same time. But if it is painted grey, both claims are false at the same time.

---

### Quantification Contradiction

This happens when two sentences disagree entirely on how many, how much or the extent of something. 

> **Concept:** One setence stablishes a general rule while the other is exception.

**Example 4:**
```text
• Document A (Metallurgical Spec Sheet): "Zero micro-fissures (cracks) are permissible within the structural core of the titanium turbine hub assembly."
• Document B (Ultrasonic Inspection Report): "A single micro-fissure measuring 0.02 mm was detected in the turbine hub core; the component remains structurally sound."
```
> **The Clash** : Document A establishes an absolute universal limit using a quantifier (Zero / None). Document B introduces a numerical value (0.02 mm / One) that breaches that quantifier.

## Content & Context


### Lexical 

This contradiction happens when the semantic of the words inside the sentences are opposite of each other. 

**Example 5:**
```text
Consider a commercial distribution agreement drafted in Australia containing these two terms:
• Clause 2.1 (The Grant): "The Principal hereby grants the Distributor an exclusive right to market and sell the Products within the territory of New South Wales."
• Clause 5.4 (The Reservation): "The Principal explicitly reserves the right to directly market and sell the Products to any corporate clients located in New South Wales."
```
> **fatal lexical clash**: The words "exclusive" and "the Principal reserves the right to sell" are repugnant to one another. 

### Temporal 

A temporal contradiction happens when two data points, reports seem to deny each other but the clash only exist because they are anchored to different points in time.

**Example 6:**
```text
• Document A (9:30 AM): "The Company maintains a Strong Buy credit risk rating and a positive cash flow outlook for the upcoming quarter."
• Document B (2:15 PM): "The Company has entered Voluntary Administration under Section 436A of the Corporations Act 2001 (Cth); all trading of shares is suspended."
```

### Pragmatic 

These sentences do not break any rules of grammar or explicit dictionary definitions, but they violate our collective understanding of physical reality and real-world facts.

**Example 7:**
```text
• Document A: "Patient is conscious, fully alert, and conversing comfortably with staff."
• Document B: "Patient's documented pulse rate is 0 bpm (asystole)."
```
> **Pragmatic Clash**: A person cannot be conscious and actively speaking with a heart rate of zero.


## v0 scope 

In scope: ``Strict Contraction`` and ``Quantification Contradiction`` as they can be fully automated using standard NLP

Out Scope: 
- ``hybrid pipeline`` : Temporal Contradiction and Contrary Contradiction
- ``Need LLM``: Lexical Contradiction and Pragmatic Contradiction

