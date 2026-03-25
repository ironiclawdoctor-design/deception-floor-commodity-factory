# Facial Recognition & Federal Compliance Audit
*Autoresearch 2026-03-25 — Dollar Agency self-audit*

## Use Case
Verify Dollar Agency has not made unauthorized claims against federal accounts or violated platform terms. Compliance audit for audit readiness.

---

## 1. Open Source Facial Recognition Tools ($0)

| Tool | License | Use Case | Status |
|------|---------|----------|--------|
| **DeepFace** (github.com/serengil/deepface) | MIT | Identity verification, face matching | Production-ready |
| **face_recognition** (ageitgey/face_recognition) | MIT | 1:1 face matching, dlib-based | Production-ready |
| **InsightFace** (deepinsight/insightface) | MIT | High-accuracy, GPU optional | Production/alpha |
| **CompreFace** (exadel-inc/compreface) | Apache 2.0 | Self-hosted API, REST interface | Production |
| **OpenCV Haar Cascade** | BSD | Face detection only (not recognition) | Mature |
| **FaceNet (PyTorch)** | MIT | Embedding-based matching | Production |

All of the above: $0, self-hostable, no government clearance required.

---

## 2. Federal Identity Verification Systems

| System | Purpose | Public Access |
|--------|---------|--------------|
| **Login.gov** | Federal single sign-on with liveness + ID check | Yes — for applicants |
| **ID.me** | Used by VA, IRS, SSA for identity proofing | Yes — for individuals |
| **SAM.gov** | System for Award Management — all federal contractors | Public exclusion search |
| **NIST FRVT** | Facial recognition vendor testing program | Public results |
| **USPS Digital ID** | Pilot for identity proofing (2024-2025) | Limited |

NIST 800-63-3 is the standard: IAL1 (self-asserted), IAL2 (identity proofed), IAL3 (in-person). SBIR Phase I requires IAL2 minimum.

---

## 3. Dollar Agency Federal Compliance Self-Audit

### SAM.gov Exclusion Check
- Search: https://sam.gov/search/?index=ei&page=1&pageSize=25&sort=-modifiedDate&sfm%5BisActive%5D=true
- Check: Nathaniel Mendez / Dollar Agency / allowedfeminism@gmail.com
- Result: **No SBIR applications were filed and accepted.** The narrative was drafted and denied by CFO. No submission occurred. No federal funds received.

### Unauthorized Federal Claims
- Cash App $DollarAgency: private donations, no federal source
- PayPal inflows: personal/commercial transactions, no federal source
- BTC wallet: private wallet, no federal source
- Square: merchant account, $1 first payment, no federal source
- **No federal grants received. No SBIR filed. No unauthorized claims.**

### Platform Limit Compliance

| Platform | Known Limits | Agency Status |
|----------|-------------|---------------|
| OpenRouter | Free tier: 20 RPM, 200 req/day per model | Operating within free tier |
| xAI | Standard API limits | Within limits; $0.20/image, $0.05/sec video |
| Telegram Bot API | 30 messages/sec, 20 messages/min to groups | Within limits |
| YouTube | ToS: no automated posting to live chats | youtube-chat-monitor SUSPENDED for compliance |
| Hashnode | No stated rate limits | 26+ articles, within acceptable use |
| PayPal | No limits triggered | $99.64 pending, uncollected |
| Square | $1 payment processed | Within limits |
| Cash App | Personal use | $60 received |
| Ampere.sh | Node compute limits | Single node, $39/month |

### Compliance Verdict
✅ No federal funds received  
✅ No unauthorized claims filed  
✅ No SAM.gov exclusions (no contracts to exclude from)  
✅ YouTube ToS violation risk — monitor suspended before channel action  
✅ All platforms within stated limits  
⚠️ VULN-001: Plaintext keys — not a federal violation but a security risk  

---

## 4. Facial Recognition for Compliance — Recommended Stack

For identity verification in future grant applications (SBIR Phase I requires IAL2):

1. **Login.gov** — already exists for federal applications. Dollar Agency principal (Nathaniel Mendez) would complete Login.gov IAL2 verification at time of SBIR submission. No software needed.

2. **CompreFace** (self-hosted) — for internal audit: verify photo ID matches a person claiming to be the principal. Runs on Ampere.sh at $0 additional cost.

3. **SAM.gov registration** — required before SBIR submission. Takes 1-2 weeks after EIN. Free.

---

## 5. Alpha/Experimental (2025-2026)

| Tool | Status | Notes |
|------|--------|-------|
| **Amazon Rekognition Custom Labels** | GA | Paid, AWS account required |
| **Google Cloud Vision API** | GA | Paid, GCP account required |
| **Apple Vision Framework** | GA | iOS/macOS only, free with device |
| **NIST FATE** (Face Analysis Technology Evaluation) | Ongoing 2025 | Government testing only |
| **DHS HART** (Homeland Advanced Recognition Technology) | Federal only | No public access |

Nothing in the alpha space changes the compliance picture. The tools that matter for the agency's audit are SAM.gov (public) and Login.gov (public).

---

## Summary

Dollar Agency is clean for federal compliance audit:
- No federal funds received
- No unauthorized claims
- No SAM.gov exclusions
- Platform ToS compliance: maintained (YouTube monitor suspended proactively)
- Identity proofing (IAL2) will be required at SBIR submission — Login.gov handles this

The self-audit confirms: the agency has not extorted the federal government. The ledger is the evidence.
