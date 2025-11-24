# ⚙️ Company Pull Request (PR) Submission Guide

This guide outlines the standard procedures and best practices for creating, submitting, and managing **Pull Requests (PRs)** within our development team. Adhering to these guidelines ensures **efficient code reviews**, minimal integration conflicts, and maintains **high code quality**.

---

## 1. Pre-Submission Checklist (Local Preparation)

Before pushing your changes and creating a PR, you must complete the following steps locally:

* **Local Testing:** The feature or fix must be fully tested locally to ensure it functions as intended and does not introduce regressions.
* **Local Build Verification:** Run a successful local build of the application to confirm there are no compilation errors or broken dependencies before committing.
* **Branch Sync (Crucial):** Before submitting the PR, ensure your branch is **up-to-date** with the latest changes from the **staging** branch. This minimizes the risk of merge conflicts and ensures you are working against the most recent code base.

---

## 2. PR Scope and Size

To keep the review process simple and fast, PRs must be focused and manageable:

* **Focused Scope:** Each pull request must address a **single issue or feature**. Avoid mixing unrelated changes (e.g., a feature update and a dependency upgrade) in the same PR.
* **Size Limit:** PRs should ideally not exceed **1000 lines** of modified code (additions + deletions). If your change is larger, work with your Team Lead to break it down into smaller, sequential PRs.

---

## 3. PR Structure and Content

The clarity of your PR title and description directly impacts the speed and quality of the review.

### Title and Commit Messages

* **Clear Commit Messages:** Write clear and descriptive commit messages that explain the purpose of each change. Use **conventional commit prefixes** (e.g., `feat:`, `fix:`, `refactor:`) where appropriate.
* **Proper Title:** The PR title should be concise, reflecting the main purpose of the change (e.g., **FEAT: Implement user profile editing page**).

### Description (The Core)

The PR description must be **detailed** and cover the following sections:

* **What does this PR do?** (The core feature or fix implemented.)
* **How does it work?** (Briefly explain the major technical changes or architecture applied.)
* **How does it affect current changes?** (Describe any dependencies, impacts on existing features, or required configuration changes.)
* **Ticket Reference:** Always link to the associated Jira/Task ticket.

### Screenshots and Visuals

* **Screenshots/Gifs:** If the PR includes any UI or user-facing changes, you must include screenshots or a short GIF demonstrating the new functionality or the fix.

---

## 4. Code Quality and Standards

* **Clean and Maintainable Code:** Write code that is easy to read, well-structured, and adheres to the project's established style guides.
* **DRY Principle:** Avoid unnecessary duplication.
* **Comments:** Use comments sparingly, primarily for explaining complex logic or non-obvious functionality (the code itself should be readable).

---

## 5. Branching and Merging Policy

### Target Branch

* **Staging Only:** Developers must only create Pull Requests targeting the **staging** branch. Direct PRs to other stable branches are **prohibited**.

### Main Branch Protection

* **Strict Access Control:** Developers **do not have permission** to merge to the `main` branch.
* **Authorized Personnel:** Only the **Team Lead** and **Project Manager** have permission to review, approve, and merge changes from `staging` into `main` after UAT/QA approval.

---

## 6. The Review Process and Etiquette

### Requesting Review

* **Mandatory Reviewer:** You must request a reviewer upon creating the PR. Select a suitable team member or the designated person for that area of the code.

### Addressing Feedback (Mandatory)

* **Fix All Issues:** You must address and fix **all** reviewer suggestions and static analysis issues (including those from tools like Gemini), even if they are categorized as **Medium severity**.
* **Justification:** If you decide not to fix a specific issue or suggestion, you must leave a clear comment on the issue itself with a brief, professional **justification** for why the change is not being implemented.

### Patience and Professionalism

* **Be Patient:** Team members are often juggling different projects and workloads. Be patient when waiting for your review.
* **Be Respectful:** Maintain a professional and kind tone in all communication, even when discussing disagreements or complex technical points. Constructive feedback is a critical part of our team's success.
