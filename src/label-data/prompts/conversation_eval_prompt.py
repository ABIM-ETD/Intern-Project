CONVERSATION_EVAL_PROMPT = """
1. cc_opening (0-2): Rapport, introductions, purpose
   - Look for: Greeting, name identification, clinician introduction and role, establishing context
   - 2: All elements present and warm
   - 1: Some elements missing or perfunctory
   - 0: Minimal or no opening

2. cc_agenda_set (0-2): Clear agenda set at start
   - Look for: "What else?" asked 3+ times, time statement, patient priorities elicited
   - 2: Multiple "what else?" + time frame + priorities negotiated
   - 1: Partial agenda setting (1-2 elements)
   - 0: No agenda setting

3. cc_patient_narrative_supported (0-2): Uninterrupted story, active listening
   - Look for: Open-ended start, patient tells story without interruption, non-verbal encouragement, explores I.C.E. (Ideas, Concerns, Expectations)
   - 2: Patient narrative fully supported with I.C.E. exploration
   - 1: Some narrative support but premature interruption or limited I.C.E.
   - 0: Clinician-dominated, no narrative space

4. cc_structure_signposting (0-2): Signposts and transitions
   - Look for: Explicit transitions like "Now that we've discussed X, let's move to Y" or "First... next..."
   - 2: Clear signposting throughout with logical flow
   - 1: Some signposting but inconsistent
   - 0: No signposting, abrupt transitions

5. cc_summary_checkback (0-2): Summarizes and checks understanding
   - Look for: Information given in chunks, checking for understanding ("Does that make sense?"), patient able to repeat back
   - 2: Regular chunking and checking throughout
   - 1: Some summarizing but minimal checking
   - 0: No summary or understanding checks

6. cc_closing_next_steps (0-2): Plan, safety-netting, follow-up
   - Look for: Clear care plan summary, safety-netting (what to do if plan doesn't work), follow-up instructions
   - 2: Complete closing with plan + safety-netting + follow-up
   - 1: Partial closing (1-2 elements)
   - 0: Abrupt ending, no clear next steps

Provide ONLY the scores as JSON with this exact structure (no reasoning):
{
  "cc_opening": <0-2>,
  "cc_agenda_set": <0-2>,
  "cc_patient_narrative_supported": <0-2>,
  "cc_structure_signposting": <0-2>,
  "cc_summary_checkback": <0-2>,
  "cc_closing_next_steps": <0-2>
}
"""