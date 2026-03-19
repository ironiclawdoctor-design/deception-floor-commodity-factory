# Token Rotation Incident — 2026-03-19 14:57 UTC

## Token Used
- **Token:** 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
- **User:** ironiclawdoctor-design
- **Purpose:** Deploy landing page to GitHub
- **Scope Issue:** Token missing `repo` scope (403 Forbidden on createRepository)
- **Status:** FAILED (insufficient permissions)
- **Action:** Token should be revoked immediately via https://github.com/settings/tokens

## What Happened
1. Token provided by user (raw failure data)
2. Verified auth status (success)
3. Attempted repo creation via gh CLI (GraphQL: Resource not accessible)
4. Attempted repo creation via REST API (403: Resource not accessible)
5. Token does not have `repo` scope needed for repository creation
6. Token cleared from environment and history

## Next Steps
1. User revokes this token at https://github.com/settings/tokens
2. User creates new PAT with `repo` scope (public_repo only)
3. Re-run deployment with correct scopes

## Lesson
- Fiesta risk assumption correct: treat all tokens as breach data
- Token scope validation before use would have caught this
- Always request minimal scopes (public_repo, not full repo)
