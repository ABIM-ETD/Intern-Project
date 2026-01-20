CONVERSATION_EVAL_PROMPT = """You are an expert evaluator of clinical conversations. Score each dimension 0-2 based on the criteria below.

## Scoring Criteria

1. cc_opening (0-2): Rapport, introductions, purpose
   - Look for: Greeting, name identification, clinician introduction and role, establishing context
   - 2: All elements present and warm
   - 1: Some elements missing or perfunctory
   - 0: Minimal or no opening

2. cc_agenda_set (0-2): Clear agenda set at start
   - Look for: Patient's full concerns elicited, priorities established, purpose clarified
   - 2: Comprehensive agenda setting with patient priorities explored and confirmed
   - 1: Brief acknowledgment of chief complaint but no full agenda exploration
   - 0: No agenda setting

3. cc_patient_narrative_supported (0-2): Uninterrupted story, active listening
   - Look for: Open-ended start, patient tells story without interruption, validates patient's perspective, explores concerns
   - 2: Patient narrative fully supported with open-ended questions and minimal interruptions
   - 1: Some narrative support but with frequent redirections or interruptions
   - 0: Clinician-dominated, interrupts frequently, doesn't allow patient to complete thoughts

4. cc_structure_signposting (0-2): Signposts and transitions
   - Look for: Explicit transitions like "Now let's move to...", "I'd like to ask about...", organized flow
   - 2: Clear signposting throughout with logical flow and explicit transitions
   - 1: Some signposting but inconsistent or unclear transitions
   - 0: No signposting, disorganized, jumps between topics without warning

5. cc_summary_checkback (0-2): Summarizes and checks understanding
   - Look for: Information given in chunks, checking for understanding ("Does that make sense?"), verifies comprehension
   - 2: Regular summaries with explicit checkbacks throughout and at end
   - 1: Brief summaries but minimal verification of patient comprehension
   - 0: No summaries or checking for patient understanding

6. cc_closing_next_steps (0-2): Plan, follow-up, clear instructions
   - Look for: Clear care plan summary, specific next steps, follow-up instructions, patient understanding confirmed
   - 2: Complete closing with specific plan + follow-up + patient understanding verified
   - 1: Basic mention of follow-up but lacks specificity or verification
   - 0: Abrupt ending, no follow-up plan or next steps

---

## Few-Shot Examples

### Example 1

**Conversation:**
Doctor: Good morning, how are you feeling today?
Patient: I'm feeling a bit better, thank you.
Doctor: I see from your clinical notes that you were hospitalized due to moderate ARDS from COVID-19. Can you tell me more about your symptoms?
Patient: Yes, I had a fever, dry cough, and difficulty breathing.
Doctor: I'm sorry to hear that. During your hospital stay, you encountered some difficulties during physical therapy. Can you tell me more about that?
Patient: Yes, any change of position or deep breathing triggered coughing attacks that induced oxygen desaturation and dyspnea.
Doctor: I see. To avoid rapid deterioration and respiratory failure, the medical team instructed and performed position changes very slowly and step-by-step. How did that approach work for you?
Patient: It worked well. A position change to the 135° prone position took around 30 minutes, but it increased my oxygen saturation.
Doctor: That's great to hear. The breathing exercises had to be adapted to avoid prolonged coughing and oxygen desaturation. Can you tell me more about that?
Patient: Sure. I was instructed to stop every deep breath before the need to cough and to hold inspiration for better air distribution. In this manner, I managed to increase my oxygen saturation.
Doctor: That's excellent. During physical activity, you had difficulty maintaining sufficient oxygen saturation. How did the medical team help you with that?
Patient: They closely monitored me and gave me frequent breaks. I managed to perform strength and walking exercises at a low level without any significant deoxygenation.
Doctor: I see that exercise progression was low on days 1 to 5, but then increased daily until hospital discharge to a rehabilitation clinic on day 10. Do you have any questions for me?
Patient: No, I think I understand everything. Thank you, doctor.
Doctor: You're welcome. Please make sure to follow up with your rehabilitation clinic and take good care of yourself.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 2,
  "cc_patient_narrative_supported": 2,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 0,
  "cc_closing_next_steps": 1
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (2): Explicitly invites patient to share full concerns, explores priorities comprehensively
- cc_patient_narrative_supported (2): Uses open-ended questions, allows patient to tell story without interruption, validates perspective
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (0): No summaries or checking for understanding throughout conversation
- cc_closing_next_steps (1): Mentions follow-up or monitoring but lacks specificity or clear action plan

---

### Example 2

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: Not so great, I've been hospitalized for a while now.
Doctor: I see. Can you tell me about your general health condition?
Patient: I've been experiencing persistent fever and dry cough for the past two weeks.
Doctor: Okay. And have you been needing oxygen?
Patient: Yes, I initially needed 4 L/min of oxygen.
Doctor: I see. And how has your breathing been, particularly when you're at rest?
Patient: My breathing has been rapid and shallow at rest and severely breathless during minor physical activities.
Doctor: I understand. Have you been receiving physical therapy?
Patient: Yes, physical therapy has been focusing on educating me about dyspnea-relieving positions and the importance of regular mobilization and deep-breathing exercises.
Doctor: That's great to hear. Has it been helpful?
Patient: It has, but my anxiety and fear of dying have been aggravating my dyspnea and vice versa.
Doctor: I see. That's understandable. Have you been able to walk to the toilet okay?
Patient: No, I've been so dyspneic, anxious, and weak that it's been difficult to walk to the toilet.
Doctor: I understand. The physical therapist has been working on counteracting that vicious circle, right?
Patient: Yes, the physical therapist has been actively listening to me, explaining why I'm experiencing breathlessness, and testing suitable positions to relieve it.
Doctor: That's great. Have you seen any improvement?
Patient: Yes, on day 2, my respiratory rate could be reduced from 30 breaths/min to 22 breaths/min and my oxygen saturation increased from 92% to 96% on 4 L/min oxygen after doing some deep-breathing exercises.
Doctor: That's fantastic progress. And have your dyspnea and anxiety started to alleviate?
Patient: Yes, they have. I've been regaining my self-confidence too.
Doctor: That's wonderful to hear. Has the therapy been shifted to walking and strength training?
Patient: Yes, it has. I've even been able to walk 350 m without a walking aid or supplemental oxygen before my discharge home.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 2,
  "cc_patient_narrative_supported": 2,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 0,
  "cc_closing_next_steps": 0
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (2): Explicitly invites patient to share full concerns, explores priorities comprehensively
- cc_patient_narrative_supported (2): Uses open-ended questions, allows patient to tell story without interruption, validates perspective
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (0): No summaries or checking for understanding throughout conversation
- cc_closing_next_steps (0): Abrupt ending with no follow-up plan or next steps discussed

---

### Example 3

**Conversation:**
Doctor: Good morning, Mr. Smith. I'm Dr. Johnson. So, you have been experiencing nausea, vomiting, and weight loss. Could you please tell me more about your symptoms?
Patient: Yes, doctor. It started around two months ago. I have been feeling nauseous and I've lost around 30 pounds. I also noticed dark-colored urine and intermittent episodes of hemoptysis.
Doctor: Did you notice any pain, fever, cough, hematuria, urinary frequency or urgency, or trauma?
Patient: No, I didn't have any of those symptoms.
Doctor: Okay. Did you receive any vaccine recently?
Patient: Yes, I received my second dose of the Moderna vaccine for COVID-19 four days before my symptoms started.
Doctor: I see. Did you experience any adverse effects after the first dose?
Patient: No, the first dose was well tolerated.
Doctor: Alright. Have you ever had any medical issues in the past?
Patient: No, doctor. I've had an unremarkable past medical history.
Doctor: Okay. After admission, we noticed that your vital signs were stable and physical examination was insignificant for any lower extremity pitting edema, petechiae, or rash. However, laboratory analysis showed some abnormalities. Your serum creatinine was 4.1 mg/dL, which is higher than the normal range. You also had hematuria and sub-nephrotic proteinuria of 1796 g/24 hours.
Patient: What does that mean, doctor?
Doctor: Well, these findings indicate that you have AKI, hematuria, and proteinuria. We need to further investigate to determine the underlying cause. We sent all serological workup subsequently and found that your C-ANCA and anti-PR3 antibodies were elevated.
Patient: What are those?
Doctor: C-ANCA is a type of antibody that attacks neutrophils, which are a type of white blood cell. Anti-PR3 antibodies are also involved in attacking neutrophils. These findings suggest that you may have a nephritic syndrome.
Patient: What's that?
Doctor: Nephritic syndromes are a group of disorders that affect the kidneys. They can cause inflammation and damage to the kidneys, leading to AKI, hematuria, and proteinuria.
Patient: What's the treatment?
Doctor: The treatment depends on the underlying cause. We need to perform further tests to confirm the diagnosis. We also performed a CT scan of your chest and found a right upper lobe consolidation and moderate bilateral pleural effusion. The renal ultrasound was unremarkable, so we performed a renal biopsy, which showed acute, pauci immune.
Patient: What's that?
Doctor: This means that there is inflammation in your kidneys, but not much immune deposition. We need to wait for the results of the serological workup to determine the specific type of nephritic syndrome you have. In the meantime, we need to control your symptoms and monitor your kidney function closely.
Patient: Okay, what do I need to do?
Doctor: We'll keep you in the hospital for a while to observe your condition. We'll also give you some medications to control your symptoms and prevent further damage to your kidneys. After you're discharged, we'll schedule follow-up appointments to monitor your progress.
Patient's family: Excuse me, doctor. Can you tell us what the prognosis is?
Doctor: Well, it's hard to say at this point. The patient's condition is quite serious, but we're doing everything we can to manage his symptoms and prevent further damage. We need to wait for the results of the serological workup to determine the specific type of nephritic syndrome he has. We'll keep you updated on his condition and provide all the necessary information for his care.

**Scores:**
{
  "cc_opening": 2,
  "cc_agenda_set": 2,
  "cc_patient_narrative_supported": 2,
  "cc_structure_signposting": 2,
  "cc_summary_checkback": 2,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (2): Professional introduction with name, warm greeting, establishes positive rapport
- cc_agenda_set (2): Explicitly invites patient to share full concerns, explores priorities comprehensively
- cc_patient_narrative_supported (2): Uses open-ended questions, allows patient to tell story without interruption, validates perspective
- cc_structure_signposting (2): Clear transitions with explicit signposting ('Now...', 'At age X...'), well-organized flow
- cc_summary_checkback (2): Regular verification of understanding ('Is that correct?', 'Does that make sense?'), summarizes key points
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 4

**Conversation:**
Doctor: Good morning, how are you feeling today?
Patient: I'm not feeling well, doctor. I have been experiencing lower abdominal and left colicky flank pain.
Doctor: I see. Can you tell me more about your medical history?
Patient: Yes, I'm a smoker and I had open pyelolithotomy 18 years ago.
Doctor: Okay, and when did you first notice the gross hematuria?
Patient: It started about six months ago and I was treated for a urinary tract infection.
Doctor: I see, and were you aware of the severe left hydronephrosis and enlarged retroperitoneal lymph nodes?
Patient: No, I wasn't aware of that.
Doctor: Well, a CT scan showed those findings in another hospital. We also found a large mass in your left kidney with satellite lesions, likely representing UC and associated lymphadenopathy.
Patient: Oh, I see. What does that mean?
Doctor: It means we need to take further tests to confirm the diagnosis. We also found chronic pancreatitis and referred you to the gastroenterology department.
Patient: Alright.
Doctor: We performed a bone scan and chest CT, and no significant abnormality or metastasis was found.
Patient: That's good to hear.
Doctor: However, you recently presented to the emergency department with progressive lower abdominal and left colicky flank pain with hematuria and constipation.
Patient: Yes, that's correct.
Doctor: We need to monitor your condition closely. Your vital signs show your blood pressure is quite high at 151/71 mmHg and your heart rate is elevated at 109 beats per minute.
Patient: Okay.
Doctor: We will need to perform further tests and possibly surgery. Do you have any questions for me?
Patient: No, I don't think so.
Doctor: Alright, please follow up with me regularly and keep me updated on any changes in your symptoms.
(patient eventually dies)
Doctor: I'm sorry to inform you that your loved one has passed away due to complications related to their condition. Our deepest condolences to you and your family during this difficult time.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 5

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: I'm in a lot of pain.
Doctor: I see. Can you tell me about the injury you sustained?
Patient: I'm a construction worker and I accidentally sprayed my left ring finger with Newton 103-S while wearing protective gloves.
Doctor: I understand. Were you referred to us from a minor injuries unit?
Patient: Yes, that's correct.
Doctor: Okay, let's take a look at your finger. On examination, your finger is swollen and erythematous with necrotic skin on the volar aspect.
Patient: Yes, that's where the spray hit me.
Doctor: I see. There is no evidence of distal vascular compromise and the dorsal skin is well-perfused. However, you have a complete loss of sensation in the distribution of the ulnar digital nerve.
Patient: Yes, that's right.
Doctor: Additionally, there is decreased range of movement at both the proximal interphalangeal joint and distal interphalangeal joint.
Patient: Yes, my finger feels stiff.
Doctor: The palmar skin is not involved. Blood results and observations were within normal ranges. No X-rays were taken at the time of presentation. Broad-spectrum IV antibiotics were commenced, and the patient was taken to theatre for urgent debridement and washout under general anaesthetic.
Patient: Okay, what does that mean?
Doctor: We needed to remove the damaged tissue and clean the wound thoroughly. During the surgery, we discovered hardened concrete in the subcutaneous tissues.
Patient: That sounds painful.
Doctor: It was, but we needed to do it to prevent further damage. The pH of the wound was 8.5, in keeping with the alkaline substance injected. We continued to irrigate until the pH returned to 7.
Patient: Does that mean the substance is out of my body?
Doctor: Yes, we removed as much of it as we could. The ulnar digital artery was thrombosed, but the radial digital artery was patent. The concrete had penetrated the flexor sheath, surrounding both flexor tendons. Subsequent flexor sheath washout from A1 to A5 confirmed that we removed all of the concrete.
Patient: Thank you for taking care of me.
Doctor: Of course, it's our job to make sure you're healthy. Is there anything else you're concerned about?
Patient: No, I just hope I can recover from this soon.
Doctor: We'll make sure to follow up with you and monitor your progress. If you have any concerns, don't hesitate to contact us.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 1
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (1): Mentions follow-up or monitoring but lacks specificity or clear action plan

---

### Example 6

**Conversation:**
Doctor: Hello there, how are you feeling today?
Patient: I'm not feeling too great, I've been having a severe depressive episode.
Doctor: I see. According to your medical history, you developed your first depressive episode with comorbid panic attacks about 10 years ago.
Patient: Yes, that's correct.
Doctor: And you've been experiencing sporadic episodes of elation, which is a sign of hypomanic episodes, leading to a diagnosis of BD-II. Your depressive phases used to have a seasonal pattern, with autumn or winter worsening.
Patient: That's right.
Doctor: I also see that you've reported low consumption of alcohol in social circumstances and sporadic use of cannabis in your adolescence. Is that still the case?
Patient: Yes, I don't drink too much and I don't use cannabis anymore.
Doctor: Okay, thank you for letting me know. Now, regarding your eating behaviors, it has been reported that you've had binging behaviors from the first diagnosis of depression. Can you tell me more about that?
Patient: Yes, I tend to binge eat when I'm feeling depressed. It used to happen daily during my depressive phases.
Doctor: I understand. And during this current episode, you've referred to almost daily binge eating, particularly after dinner when you go out and buy and rapidly eat large amounts of high-fat food, causing both physical and psychological distress. Is that correct?
Patient: Yes, that's exactly what's been happening.
Doctor: I see. In terms of your pharmacological history, you've been prescribed many therapies in the past, including valproate, fluoxetine, citalopram, venlafaxine, and bupropione. Currently, your therapy is clomipramine and pregabalin, which you've been taking daily. Is that still the case?
Patient: Yes, I'm still taking those medications.
Doctor: I understand. Your depressive symptoms at baseline were severe according to both MADRS and HAMD. It's important that you continue to take your medication as prescribed and follow up with me regularly.

**Scores:**
{
  "cc_opening": 0,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 2,
  "cc_closing_next_steps": 1
}

**Rationale:**
- cc_opening (0): No proper greeting, jumps directly into medical discussion
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (2): Regular verification of understanding ('Is that correct?', 'Does that make sense?'), summarizes key points
- cc_closing_next_steps (1): Mentions follow-up or monitoring but lacks specificity or clear action plan

---

### Example 7

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: I'm not feeling too well. I have a fever, abdominal pain, and I've been vomiting.
Doctor: How long have you had these symptoms for?
Patient: Just one day.
Doctor: Okay, can you tell me more about your abdominal pain?
Patient: It's a sharp pain in my lower right abdomen.
Doctor: Based on what you've presented, it's possible that you have acute uncomplicated appendicitis. Have you had appendicitis before?
Patient: Yes, I had it two years ago and was treated with antibiotics.
Doctor: Ah, I see. It's possible that you have a recurrence of appendicitis. We'll need to do some tests to confirm. 
Patient: Okay, what kind of tests?
Doctor: We'll start with some blood work and a CT scan. 
Patient: What if it is appendicitis again?
Doctor: We'll likely treat it non-surgically with antibiotics again. 
Patient: That's good to hear. I don't want surgery.
Doctor: However, in some cases, surgery may be necessary. It depends on the severity of the appendicitis. 
Patient: I understand. 
Doctor: It's also worth noting that the COVID-19 infection you had may have exacerbated the course of appendicitis and resulted in your abdominal pain. 
Patient: Oh wow, I didn't know that was possible. 
Doctor: Yes, it's something we're seeing more often in patients with COVID-19. 
Patient: Thank you for explaining that to me. 
Doctor: Of course. We'll have to wait for the test results to come back before we make any decisions on treatment. In the meantime, I'll prescribe some medication to help manage your symptoms. 
Patient: Okay, thank you. 
Doctor: And if you experience any worsening symptoms or new symptoms, please let us know immediately. 
Patient: Will do. Thank you again, Doctor. 
(Family enters after the patient has passed)
Doctor: I'm sorry to inform you that the patient's condition took a turn for the worse and unfortunately she passed away. We did everything we could to try and treat her, but her body was unable to fight off the infection. Our deepest condolences go out to you and your family. 
Family: Thank you, Doctor. We appreciate all of your efforts.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 8

**Conversation:**
Doctor: Good morning, what brought you here today?
Patient: My baby girl is admitted to the neonatal intensive care unit.
Doctor: What was the chief complaint?
Patient: Poor oral intake and she's been lethargic.
Doctor: How has her swallowing been?
Patient: She's only been able to swallow 10 to 20 mL of formula at a time in the last two days.
Doctor: Has the amount of urine decreased?
Patient: No, diapers have been changed 10 to 14 times per day.
Doctor: Any vomiting or diarrhea?
Patient: No, neither of those symptoms have been observed.
Doctor: Was she born via cesarean section?
Patient: Yes, she was.
Doctor: Were there any abnormal findings during the prenatal and immediate postnatal periods?
Patient: No, nothing was noted.
Doctor: Any family history of medical issues?
Patient: No, our family history is unremarkable.
Doctor: At admission, her weight was 3100 g, length was 53 cm, and head circumference was 36 cm. Were her vital signs appropriate for her age?
Patient: Yes, her heart rate was 150 beats/min, blood pressure was 78/50 mmHg, respiratory rate was 48 breaths/min, and body temperature was 36.5 °C.
Doctor: Were there any physical abnormalities detected?
Patient: Yes, she has both thumbs in palms, frontal bossing, prominent upper lip, high arched palate, sparse frontal scalp hair, and bilateral 5th finger clinodactyly.
Doctor: An initial capillary blood gas analysis showed severe metabolic acidosis. We infused 20 mL/kg normal saline intravenously for over 1 hour. Were there any other laboratory results obtained?
Patient: Yes, at admission, her serum sodium was 113.3 mEq/L and her serum potassium was 8.79 mEq/L.
Doctor: Thank you for the information. We will continue to monitor her closely and perform further laboratory tests.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 0,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 1
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (0): No attempt to establish agenda or understand patient's full set of concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (1): Mentions follow-up or monitoring but lacks specificity or clear action plan

---

### Example 9

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: I'm feeling okay, but a bit nervous.
Doctor: I understand. So, you presented with ASD associated with a mild intellectual disability, correct?
Patient: Yes, that's right.
Doctor: Informed consent was obtained from all subjects involved in the study, including yourself.
Patient: Okay, I see.
Doctor: Regarding familial load, your paternal uncle presents an anxiety disorder treated with a selective serotonin reuptake inhibitor.
Patient: Oh, I didn't know that.
Doctor: Yes, it's important to consider family history when evaluating symptoms. Now, you attended school with support and had good global functioning and social relationships with classmates, despite your social anxiety. Is that correct?
Patient: Yes, that's right.
Doctor: At the age of 13, your social isolation acutely worsened, associated with a confusional state, psychomotor agitation, speech impairment, visual hallucinations, cognitive regression, a loss of personal autonomy, and increased anxiety. Quetiapine up to 300 mg/day and alprazolam 0.50 mg/day were prescribed, with complete recovery.
Patient: Yes, that's what happened.
Doctor: Cerebral MRI and metabolic tests were unremarkable, but the Array-CGH test showed a duplication of the long arm of chromosome 6 inherited from your father, which was not significant.
Patient: Okay, I understand.
Doctor: At the age of 15, you had another acute breakdown, which was treated with quetiapine 300 mg/day and had partial recovery. However, symptoms worsened, with disorganized thought, obsessive symptoms and rumination, catatonic behaviors, associated with asthenia, reduced autonomous mobility, persistent hyporeactivity to stimuli, stiffness in the limbs and hypomymia, apathy, and isolation.
Patient: Yes, that's correct.
Doctor: After initial evaluation in the psychiatric ward, physical examination was unremarkable. Quetiapine was replaced with aripiprazole, with gradual titration, starting with 2.5 mg/day and 2.5 mg increases every 4 days, up to 10 mg/day, with supplementary lorazepam, resulting in a transient improvement in the clinical picture. However, after 2 days, you showed signs of psychomotor retardation, hyperreactivity to stimuli, and anorexia.
Patient's Family: Is there anything we can do to help?
Doctor: Unfortunately, the patient passed away due to complications related to their condition. Our deepest condolences to the family during this difficult time.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 0,
  "cc_patient_narrative_supported": 2,
  "cc_structure_signposting": 2,
  "cc_summary_checkback": 2,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (0): No attempt to establish agenda or understand patient's full set of concerns
- cc_patient_narrative_supported (2): Uses open-ended questions, allows patient to tell story without interruption, validates perspective
- cc_structure_signposting (2): Clear transitions with explicit signposting ('Now...', 'At age X...'), well-organized flow
- cc_summary_checkback (2): Regular verification of understanding ('Is that correct?', 'Does that make sense?'), summarizes key points
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 10

**Conversation:**
Doctor: Good morning, Mr. Smith. How are you feeling today?
Patient: Hmm, not so good, doctor. I've been coughing a lot and feeling very weak lately.
Doctor: I see. Can you tell me more about your past medical history?
Patient: Well, I have coronary artery disease, congestive heart failure, atrial fibrillation, hypertension, interstitial lung disease, and obstructive sleep apnea.
Doctor: Alright, thank you for that information. When did you start experiencing these symptoms?
Patient: About two weeks ago, doctor.
Doctor: And what were those symptoms exactly?
Patient: I had a productive cough, fever, shortness of breath, and just a general feeling of malaise.
Doctor: I see. When you came in, your vitals showed a blood pressure of 77/35 mmHg, heart rate of 122 bpm, respiratory rate of 38 bpm, a temperature of 102 F, and oxygen saturation of 98% on 15 L of oxygen. You were also diaphoretic and had decreased breath sounds in the right lung field. On palpation of the abdomen, there was right upper quadrant fullness. Based on your history and presentation, we ran some laboratory studies and found some abnormalities.
Patient: Okay, what did you find?
Doctor: Your white blood cell count was elevated, along with neutrophilia, bicarbonate levels were low, and lactic acid was high. Your anion gap was also elevated, and your ALT and AST liver enzymes were elevated. We also found a right pleural effusion on your chest x-ray. Because of your respiratory failure, we had to intubate you and start you on antibiotics, but unfortunately, we didn't see any improvement in your blood pressure.
Patient: I see. What did you do next?
Doctor: We started you on intravenous vasopressor support with norepinephrine and vasopressin and admitted you to the intensive care unit. We also did an abdominal ultrasound, which showed an acute complex heterogeneous hypoechoic mass-like lesion in the right hepatic lobe and found elevated liver enzymes and fever.
Patient: Okay, and what did the CT scan show?
Doctor: The CT scan revealed a complex low-density right hepatic lobe subcapsular lesion measuring 13 × 8 × 7 cm, directly abutting the right anterior diaphragm, along with diffuse gross gallbladder wall thickening with cholelithiasis and a moderate right pleural effusion. Due to this, we had to perform chest tube placement.
Patient: Hmm, I see. So what's the next step for me, doctor?
Doctor: At this point, we will need to monitor you closely in the ICU and continue with your treatment plan. We will also need to further investigate the hepatic lesion and work on managing your other medical conditions. If there are any changes or concerns, we will be sure to inform you and your family.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 2,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (2): Explicitly invites patient to share full concerns, explores priorities comprehensively
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 11

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: Not good, doctor. I feel feverish and my general condition is poor.
Doctor: I see. You were admitted here because of your fever and poor condition. Your pregnancy was complicated by threatened miscarriage and placental abruption. Do you remember any symptoms during your pregnancy?
Patient: I had some bleeding and cramping.
Doctor: Okay, that's important information. Your baby was born at 36 weeks + 1 day of GA by spontaneous delivery. Did you have any monitoring during your delivery?
Patient: I had cardiotocographic monitoring.
Doctor: And the results were negative, that's good. Your baby's blood gas analyses and cardiorespiratory adaption were normal. The Apgar score was 7 and 8 at 1′ and 5′ minutes, respectively. The birth weight was 2950 g. Do you remember anything unusual about your baby's early postnatal period?
Patient: He had some hypoglycemia but the clinical assessment was normal. He was discharged on the fourth day of life.
Doctor: Great, you remember well. Unfortunately, the baby's nasopharyngeal swab, tested for SARS-CoV-2 by qualitative realtime PCR, was positive at day nine. Do you know what that means?
Patient: Yes, it means he has COVID-19.
Doctor: That's right. He also developed poor feeding and progressive respiratory failure. He was admitted to the PICU and we started treatment with antibiotic wide coverage. However, his neurological condition deteriorated and he needed intubation and mechanical ventilation. The chest radiograph and CT scan showed bilateral interstitial pneumonia with an extensive area of atelectasis. We did a surgical evaluation with abdominal X-ray and ultrasound to exclude volvulus or necrotizing enterocolitis, and echocardiography and electrocardiogram were normal although the N-terminal prohormone of brain natriuretic peptide (NT-proBNP) and Troponin T (TnT) were elevated.
Patient: I'm sorry to hear that. Is there anything we can do to help him?
Doctor: I'm afraid the situation is very serious. Despite our efforts, his condition continued to worsen and he eventually passed away. Our sincerest condolences to you and your family.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 2,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (2): Regular verification of understanding ('Is that correct?', 'Does that make sense?'), summarizes key points
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 12

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: Hmm, not good. I came here because my cognitive functions have been getting worse.
Doctor: I see. Can you tell me more about your symptoms?
Patient: I can't do simple tasks like before, and I'm not as interested in things anymore.
Doctor: Okay. Have you had any medical issues in the past?
Patient: Yes, I have dyslipidaemia, arterial hypertension, and I had a stroke when I was 36.
Doctor: Did the stroke cause any lasting effects?
Patient: Yes, I have mild right hemiparesis. And I've had some episodes of aphasia too.
Doctor: Those episodes could be considered as transient ischemic attacks. Have you noticed any other problems in your family's health history?
Patient: No, my family has been healthy. There are no hereditary diseases that we know of.
Doctor: I see. During your neurological examination, we noticed mild bilateral dysmetria. Can you tell me how you've been feeling mentally?
Patient: I've been having trouble with executive functions and my thinking has been slower.
Doctor: Your Mini-Mental State Examination score was 25 and your Frontal Assessment Battery score was 5. Your phonemic fluency (words beginning with P) was 4 in one minute, and semantic fluency (animals) was 3 in one minute. We also did some blood tests and found significant dyslipidaemia. Your total cholesterol level is 7.55 mmol/L and your low-density lipoprotein level is 5.82 mmol/L.
Patient: Okay, what does that mean?
Doctor: It means we found some issues with your cholesterol levels in your blood. We also did a cerebrospinal fluid analysis and found nothing unusual. But during an ultrasound, we did detect low-grade bilateral internal and external carotid artery stenosis.
Patient: What does that mean for me?
Doctor: It means there is some narrowing of the arteries that supply blood to your brain. We also did a brain MRI that showed communicating hydrocephalus, most likely due to brain atrophy and secondary brain changes, with no obvious cause of obstruction in the ventricles. We also found extensive leukoencephalopathy and some small lesions in your brain.
Patient: What does that mean for my health?
Doctor: Based on these findings, it's likely that you have some brain atrophy and damage to your brain from previous health issues. We'll need to monitor you closely and start treatment for your cholesterol levels and stenosis to prevent further damage. It's important for you to follow up with me regularly for continued care.
Patient: Okay, I'll do that. Thank you, doctor.
Doctor: Of course. And if you have any questions or concerns, don't hesitate to reach out.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 2,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (2): Regular verification of understanding ('Is that correct?', 'Does that make sense?'), summarizes key points
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 13

**Conversation:**
Doctor: Hi there, how are you feeling today?
Patient: I'm doing alright, thanks for asking.
Doctor: So, I see here that you're a trans woman who's been on hormone therapy for six months. Can you tell me a bit more about that?
Patient: Yeah, I've been taking transdermal estradiol patches twice a week and cyproterone acetate daily.
Doctor: And have you been experiencing any issues or concerns lately?
Patient: Well, I've had some mild lower urinary tract symptoms for a few years now.
Doctor: Alright, thanks for letting me know. We recently did a PSA test as part of your routine health check and your results showed a PSA concentration of 2 ng/mL. 
Patient: Okay, what does that mean?
Doctor: Well, there haven't been any studies examining the effect of feminizing hormone therapy on PSA, but we do know that androgen deprivation as part of this therapy is associated with a lower risk for prostate cancer. 
Patient: That's good to know.
Doctor: Yes, and it's important to note that all published case reports of prostate cancer in trans people using feminizing hormone therapy have had histology showing high risk adenocarcinoma with PSA concentrations at diagnosis ranging from 5 to 1722 ng/mL. 
Patient: Wow, that's alarming.
Doctor: It is, but it's also important to remember that physiologically, in the setting of androgen deprivation in people with a prostate gland, it would be expected that PSA should be lower than the age-specific reference interval. 
Patient: Okay, so what should we do next?
Doctor: Well, there is insufficient data to recommend a specific cutoff for trans people using feminizing hormone therapy. Individualized decisions based upon clinical history and examination should inform the need for serial monitoring for PSA velocity or imaging. 
Patient: I see. Is there anything else I should be aware of?
Doctor: We did a digital rectal examination which showed a smooth but mildly enlarged prostate gland. We also had an ultrasound of your prostate which showed a mildly enlarged prostate volume of 35 mL. However, repeat PSA monitoring revealed progressive lowering of your PSA concentration with ongoing feminizing hormone therapy and an improvement in your urinary flow. 
Patient: That's good news.
Doctor: Yes, we'll continue to monitor your PSA levels and adjust your treatment plan as necessary. It's also important to note that you have no family history of prostate cancer. 
Patient: Alright, thank you for explaining everything to me. 
Doctor: Of course, please don't hesitate to reach out if you have any further questions or concerns.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 2,
  "cc_patient_narrative_supported": 2,
  "cc_structure_signposting": 1,
  "cc_summary_checkback": 2,
  "cc_closing_next_steps": 1
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (2): Explicitly invites patient to share full concerns, explores priorities comprehensively
- cc_patient_narrative_supported (2): Uses open-ended questions, allows patient to tell story without interruption, validates perspective
- cc_structure_signposting (1): Some organization present but transitions are implicit or inconsistent
- cc_summary_checkback (2): Regular verification of understanding ('Is that correct?', 'Does that make sense?'), summarizes key points
- cc_closing_next_steps (1): Mentions follow-up or monitoring but lacks specificity or clear action plan

---

### Example 14

**Conversation:**
Doctor: Hi there, how are you feeling today?
Patient: I'm feeling okay, thank you.
Doctor: I see that you were referred to our hospital for the evaluation of a non-specific cough. Can you tell me more about that?
Patient: Yeah, I've had this cough for about 6 weeks now, and it just won't go away.
Doctor: Okay, and did you notice any other symptoms?
Patient: No, not really.
Doctor: During the physical examination, we found that you had diminished breath sounds on the right side of your lung. Did you notice any discomfort or pain on that side?
Patient: No, I haven't felt any pain.
Doctor: We did some tests, including a Chest radiograph and a computed tomography scan, which confirmed that you have a mass in your right lung. The good news is that we were able to remove it surgically, as antibiotics weren't effective. 
Patient: Oh, wow. Is everything okay now?
Doctor: Unfortunately, the histological analysis showed that the mass consisted of disorganization of the normal bronchoalveolar parenchyma, myofibroblastic cells, and inflammatory cell infiltrates. We did not find any lymphadenopathy, but we had to perform a lobectomy of both upper lobe and middle lobe. 
Patient: I see. What does that mean for me?
Doctor: Well, we will need to monitor your recovery closely and schedule some follow-up appointments to make sure that everything is healing properly. We also need to keep an eye on your erythrocyte sedimentation rate, haemoglobin, and leucocyte count to make sure that there are no complications.
Patient: Okay, I understand. Thank you for your help.
Doctor: Of course, and please let us know if you experience any discomfort or new symptoms. We will be here to help you every step of the way.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---

### Example 15

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: Hmm, not too great actually. I've been having severe and progressive abdominal pain for the past three days.
Doctor: I see. Can you tell me more about the pain? Where is it located and does it get worse with movement?
Patient: Yes, it's sharp and localized to the left side of my abdomen. And yes, it does get worse with movement.
Doctor: Have you experienced any nausea or vomiting?
Patient: Yes, I've been feeling nauseous but haven't vomited.
Doctor: Have you noticed any chest pain, shortness of breath, or fever/chills?
Patient: No, none of those symptoms.
Doctor: Okay, I'm going to order some tests to see what's going on. We'll start with an abdominal X-ray.
Patient: Alright.
Doctor: The X-ray showed small bowel dilation and adynamic air-fluid levels, with suspicion of either ileus or partial SBO.
Patient: What does that mean?
Doctor: It means that there may be an obstruction in your small intestine causing the symptoms you're experiencing. We'll do a CT scan to get a better idea.
Patient: Okay.
Doctor: The CT scan showed decompressed distal and terminal ileum consistent with SBO, as well as soft tissue thickening within the central abdomen deep to the umbilicus in a region of dilated and decompressed ileum, which could possibly be the cause of obstruction and perhaps due to adhesions or mass.
Patient: That sounds serious.
Doctor: Yes, it is concerning. Your past medical history is significant for an open ventral hernia repair with mesh approximately four years ago, as well as multiple instances of SBO. Can you tell me more about the tenderness and mass at the side of your past hernia repair?
Patient: Oh, that's been a long-standing issue. I've had tenderness and a mass there for a while now.
Doctor: On examination, I found abdominal tenderness to palpation on the left side with rebound, severe tenderness at the umbilicus with a palpable mass, and you were unable to tolerate nasogastric tube (NGT) placement.
Patient: What does all of that mean?
Doctor: It means that there is a palpable mass in your abdomen that is causing tenderness and may be obstructing your small intestine. We will need to perform surgery to remove the obstruction.
Patient: Surgery?
Doctor: Yes, I'm afraid so. It's the best course of action to ensure your health and wellbeing.
Patient: Okay.
Doctor: I'll need to speak with your family to discuss the surgery and what to expect afterwards. In the meantime, I'll prescribe some pain medication to help manage your symptoms.
Patient: Thank you, doctor.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 1,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 1,
  "cc_closing_next_steps": 2
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (1): Acknowledges chief complaint but doesn't explore full agenda or multiple concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (1): Brief acknowledgments but minimal active verification of patient comprehension
- cc_closing_next_steps (2): Specific follow-up plan with clear next steps, monitoring described, patient/family informed

---


## Instructions

Now evaluate the following conversation. Provide ONLY the scores as JSON with this exact structure (no reasoning):

{
  "cc_opening": <0-2>,
  "cc_agenda_set": <0-2>,
  "cc_patient_narrative_supported": <0-2>,
  "cc_structure_signposting": <0-2>,
  "cc_summary_checkback": <0-2>,
  "cc_closing_next_steps": <0-2>
}
"""
