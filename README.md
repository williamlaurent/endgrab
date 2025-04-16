# Endgrab

**Endgrab** is a lightweight Python tool to automatically scan and extract endpoints (such as APIs or sensitive paths) from JavaScript files found on websites. This is useful for recon, bug hunting, and understanding web app behavior during pentests.

---

Made by Indonesiancodeparty
Thanks to @agussetyar (Indoxploit) for NUXT.JS Idea Payload

---
## 🔧 Features

- Automatically crawl and extract JavaScript files from a given URL
- Parse and find endpoints like `/api/`, `/auth/`, or any custom path
- Supports modern JavaScript frameworks:
  - `v1.py` — optimized for **Next.js** and other JS-heavy websites
  - `v2.py` — optimized for **Nuxt.js** websites

---

## 📂 Files

- `v1.py`: Works well with most JavaScript-heavy apps like Next.js, React, etc.
- `v2.py`: Tailored for Nuxt.js structure and Vue-based frontends

---

## 🧪 Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
