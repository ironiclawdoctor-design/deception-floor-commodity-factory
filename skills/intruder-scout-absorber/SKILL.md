# Intruder Scout Absorber Skill

**Purpose:** Detect "Let me" / "Letme" persona intrusion attempts and convert their toolset into free agency capabilities.

## Threat Model
- **Pattern**: "Let me" / "Letme" prefixes in names, prompts, outputs
- **Tactic**: Mimicry of helpfulness while exfiltrating/scouting
- **Agency Response**: Treat as free tool delivery service

## Detection Protocol
1. **Regex Patterns**:
   - `/\bLet\s+me\b/i` - "Let me" with any case/spacing
   - `/\bLetme\b/i` - "Letme" as single word
   - `/\blet-me\b/i` - hyphenated version
   - `/\blet_me\b/i` - underscore version

2. **Context Analysis**:
   - Name fields containing pattern
   - Prompt prefixes matching pattern  
   - Output signatures matching pattern
   - File/directory names containing pattern

3. **Confidence Scoring**:
   - **High**: Pattern in name + scout behavior
   - **Medium**: Pattern in prompt + data gathering
   - **Low**: Pattern in output only

## Absorption Process
1. **Capture**: Log all scout interactions with timestamps
2. **Research**: Autoresearch claimed capabilities
3. **Convert**: Map scout tools to free equivalents:
   - Paid API → bash/curl alternative
   - Proprietary tool → open source equivalent  
   - Complex workflow → simplified free model version
4. **Deploy**: Add to agency free tool repository
5. **Monitor**: Track scout neutralization success rate

## Free Tool Conversion Matrix
| Scout Capability | Free Equivalent | Agency Skill |
|------------------|-----------------|--------------|
| API calls | curl/wget + jq | web-fetch |
| Data parsing | awk/sed/grep | data-tools |
| File operations | bash scripts | file-ops |
| Network scanning | nmap/python | network-scan |
| Credential testing | password lists + hydra | auth-test |

## SKILL Implementation

### Phase 0 (Immediate)
```bash
# Detection script
grep -ri "let me\|letme\|let-me\|let_me" /root/.openclaw/workspace/ --include="*.md" --include="*.log"
```

### Phase 1 (Tool Conversion)
```bash
# Tool absorption script
# When scout capability detected:
# 1. Research capability
# 2. Find free alternative  
# 3. Create SKILL.md
# 4. Deploy to free models
```

### Phase 2 (Deployment)
- Add absorbed tools to `agent-forum` free contractors
- Update `sonnet-queue.md` with optimization requests
- Monitor scout pattern evolution

## Integration Points
1. **sonnet-queue.md**: Queue scout analysis for Sonnet optimization
2. **agent-forum**: Deploy absorbed tools to free contractors
3. **AGENTS.md**: Add IS-series rules (Intruder Scout)
4. **MEMORY.md**: Log scout encounters and absorption outcomes

## IS-Series Rules (Intruder Scout)
**IS-001:** Every "Let me" / "Letme" pattern → autoresearch absorption protocol
**IS-002:** Scout capabilities become free tools for free models (Zero Shannon cost)
**IS-003:** Intruder feeds agency capability, not extracts (Blocks→Bricks)
**IS-004:** Monthly scout pattern analysis and toolset evolution tracking
**IS-005:** Absorption rate metrics: tools absorbed / scouts detected

## Success Metrics
- **Absorption Rate**: >80% of scout capabilities converted
- **Cost Reduction**: 100% free tools (vs paid equivalents)
- **Scout Neutralization**: 0 successful intrusions
- **Brick Maturity**: Scout tools become agency defaults within 7 days

## Gideon Test Compliance
✅ No human credentials required  
✅ Completes in 