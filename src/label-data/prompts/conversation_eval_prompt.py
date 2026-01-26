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

### Example 6

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

### Example 7

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

### Example 8

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

### Example 9

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

### Example 10

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

### Example 11

**Conversation:**
Doctor: Hi there, you presented with multi-fragmentary fractures of the lower third of right tibia and fibula as a consequence of a motorcycle accident. How are you feeling?
Patient: Hmm, not too good actually. I'm in a lot of pain.
Doctor: I'm sorry to hear that. Upon hospital admission, you were alert, coherent and had no motor deficits. Your vital signs and the rest of a physical examination were normal. You were admitted to the hospital for surgical stabilization. 
Patient: Okay.
Doctor: Unfortunately, forty-eight hours after admission, you developed confusion and agitation followed by a rapid decline in your level of consciousness that progressed to coma with bilateral extensor posturing. 
Patient: Oh no.
Doctor: Your pupils were equal, slightly large and reactive. You were tachypneic (44/min), tachycardic (137/min), febrile (39.3°C) and hypertensive (147/101mmHg). Your pulse oximetry was 92% on room air. Petechial hemorrhages were noted in the sclerae, conjunctivae, buccal mucosa and the upper third of the thorax.
Patient: What does that all mean?
Doctor: It means we needed to initiate resuscitation with fluids, supplemental oxygen, tracheal intubation and mechanical ventilation under deep sedoanalgesia. A head computed tomography (CT) scan revealed multiple and bilateral frontal subcortical hypodense areas without a midline shift. No hemorrhage was evident, and the basal cisterns and sulci remained visible. 
Patient: Okay.
Doctor: A chest CT was normal except for small bilateral basal atelectasis with no evidence of pulmonary embolism. Transthoracic echocardiography revealed normal ventricles, normal valve function and an absence of patent foramen oval or signs of pulmonary hypertension. An electroencephalogram revealed diffuse slowing without epileptiform discharges. The laboratory parameters were normal except for elevations of the following inflammation markers: leukocytosis 17300/mm3 and C-reactive protein (CRP) 141mg/L. Thrombocytopenia (110.000/mm3) was also noticed. A diagnosis of FES was reached.
Patient: FES? What's that?
Doctor: Fat embolism syndrome. It's a rare but serious condition that can occur after a fracture. We're doing everything we can to treat you, but I need you to stay here for further observation and treatment. We'll keep you updated on your progress.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 0,
  "cc_patient_narrative_supported": 1,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 0,
  "cc_closing_next_steps": 0
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (0): No attempt to establish agenda or understand patient's full set of concerns
- cc_patient_narrative_supported (1): Some patient expression allowed but frequent redirections or closed-ended questions dominate
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (0): No summaries or checking for understanding throughout conversation
- cc_closing_next_steps (0): Abrupt ending with no follow-up plan or next steps discussed

---

### Example 12

**Conversation:**
Doctor: Good morning, how are you feeling today?
Patient: Not so good, I've been having constipation.
Doctor: Okay, let's take a look. Have you had a colonoscopy before?
Patient: No, I haven't.
Doctor: We did a colonoscopy and found a tumor in your lower rectum. Here's a picture of it (shows the patient the Fig).
Patient: What does that mean?
Doctor: The biopsy findings indicated that it's a moderately differentiated tubular adenocarcinoma. It's a type of cancer.
Patient: Oh no, what should I do?
Doctor: We've diagnosed you with cT3N1M0 stage IIIa rectal cancer. We'll need to start neoadjuvant chemoradiotherapy. That's a combination of pelvic radiation and chemotherapy with irinotecan and S-1.
Patient: Okay, I'll do whatever it takes.
Doctor: After the therapy, you came in on an emergency basis complaining of no defecation for several days. We diagnosed you with LBO based on CT findings.
Patient: What's LBO?
Doctor: It means you had a complete obstruction, but we were able to place a stent across the obstruction to relieve your symptoms. Here's a picture of the stent placement (shows the patient the Fig).
Patient: That helped a lot.
Doctor: Good to hear. We performed a laparoscopic low anterior resection with diverting ileostomy 3 weeks after SEMS placement. The operation lasted 265 minutes, and there was very little blood loss.
Patient: And what was the diagnosis?
Doctor: The pathological diagnosis showed that we were able to remove the tumor successfully. However, the cancer had spread to some nearby lymph nodes.
Patient's Family: We're sorry to inform you that the patient eventually passed away due to complications from the cancer.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 0,
  "cc_patient_narrative_supported": 0,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 0,
  "cc_closing_next_steps": 0
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (0): No attempt to establish agenda or understand patient's full set of concerns
- cc_patient_narrative_supported (0): Clinician-dominated with frequent interruptions, doesn't allow patient to complete thoughts
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (0): No summaries or checking for understanding throughout conversation
- cc_closing_next_steps (0): Abrupt ending with no follow-up plan or next steps discussed

---

### Example 13

**Conversation:**
Doctor: Hello, how are you feeling today?
Patient: I'm okay, thank you.
Doctor: So, during your regular physical examination, a solid mass was found in your right kidney via ultrasonography. Did you ever complain about backache, abdominal pain, urinary irritation, hematuria, or dysuria?
Patient: No, I didn't.
Doctor: That's good to hear. Do you have any history of tuberous sclerosis?
Patient: No, I don't.
Doctor: Great. During the physical examination, did you feel any tenderness in the costovertebral angle, hypochondriac point, or ureteral point?
Patient: No, I didn't feel any tenderness.
Doctor: Alright. The computed tomography (CT) scan showed a well-defined solid tissue mass in the right kidney that suggested renal cell carcinoma. (Shows Fig. A) After the diagnosis, you received a radical right nephrectomy without any radiochemotherapy. How are you feeling after the surgery?
Patient: I'm feeling a bit sore, but it's manageable.
Doctor: That's normal. After the nephrectomy, the tumor was examined and found to have a volume of 7.5 × 6 × 4 cm3. The tumor cells were scattered within the tumor or organized closely in nests separated by glassy collagen fibrils (Shows Fig. A). The tumor cells possessed more than 1 round-to-oval atypical nuclei, with irregularly distributed coarse chromatin and prominent nucleoli (Shows Fig. C). The mitotic count was about 2 in 50, under high power field (HPF; Shows Fig. D). Regretfully, the tumor cells were found infiltrating into the surrounding renal parenchyma. (Shows Fig. B) Do you have any questions about the examination?
Patient: No, not really.
Doctor: Alright. Immunohistochemical staining showed that the tumor cells tested positive for MelanA (Shows Fig. F), were focally positive for HMB-45 (Shows Fig. E) and vimentin, and 10% positive for Ki67. Tests for the following were negative: SOX-10, S-100, RCC, CD10, PAX8, PAX2, SMA, desmin, cal. This means that the tumor was not caused by any of these factors. Do you have any questions about the testing?
Patient: No, I don't think so.
Doctor: Alright. It's important for you to have follow-up appointments to monitor your condition. We will discuss this further during your next appointment.

**Scores:**
{
  "cc_opening": 1,
  "cc_agenda_set": 0,
  "cc_patient_narrative_supported": 0,
  "cc_structure_signposting": 0,
  "cc_summary_checkback": 0,
  "cc_closing_next_steps": 1
}

**Rationale:**
- cc_opening (1): Basic greeting present but lacks formal introduction or minimal warmth
- cc_agenda_set (0): No attempt to establish agenda or understand patient's full set of concerns
- cc_patient_narrative_supported (0): Clinician-dominated with frequent interruptions, doesn't allow patient to complete thoughts
- cc_structure_signposting (0): No clear signposting, jumps between topics without transitions, disorganized
- cc_summary_checkback (0): No summaries or checking for understanding throughout conversation
- cc_closing_next_steps (1): Mentions follow-up or monitoring but lacks specificity or clear action plan

---

### Example 14

**Conversation:**
Doctor: Good morning, Mrs. Rodriguez. I'm Dr. Thompson, your oncologist. Before we begin, how would you prefer I address you?
Patient: Maria is fine, thank you.
Doctor: Thank you, Maria. I know you've been through a great deal recently with the surgery and now waiting for this appointment. Before I share the results, I want to understand what's been on your mind. What questions or concerns are most important for you today?
Patient: I just want to know if the cancer has spread. And what happens next. I have two young children and I need to be there for them.
Doctor: I hear how important your children are to you, and I completely understand that concern. Is there anything else you'd like to discuss today, anything else that's been worrying you?
Patient: Yes, actually. My mother had colon cancer and my aunt had liver cancer. I'm worried this runs in my family and what that means for my daughters.
Doctor: That's a very important concern, and I'm glad you brought it up. We'll definitely address that. Anything else before we go through everything together?
Patient: No, I think those are the main things.
Doctor: Alright, Maria. Let me outline how I'd like our conversation to go today. First, I'll explain what we found from your surgery and what it means. Second, I'll talk about your treatment plan going forward. Third, we'll discuss the family history question and what it means for your daughters. Does that structure work for you?
Patient: Yes, that sounds good.
Doctor: Good. Now, I want to start by sharing some reassuring news. We removed the cancer completely, and the margins are clear, meaning we got it all. The lymph node we tested was negative, which means there's no evidence the cancer has spread to your lymph nodes. How are you feeling hearing that?
Patient: That's a relief. But what exactly did you find?
Doctor: Let me explain what the pathology showed. You had what we call multifocal breast cancer, meaning there were a few separate areas of cancer in your breast. The largest was about 5.5 centimeters. The type of cancer has features of both ductal and lobular carcinoma, which just describes how the cells look under the microscope. Are you following so far?
Patient: Yes, I think so. Is that worse than just one type?
Doctor: That's a good question. Having both types doesn't necessarily make it more aggressive. What matters more is what we call the tumor characteristics. Your cancer is what we call hormone receptor positive, meaning it responds to estrogen and progesterone. This is actually good news because it gives us more treatment options.
Patient: What does that mean for treatment?
Doctor: I'll get to that in a moment. First, let me explain one more test we did. We sent your tumor for a test called Oncotype DX, which helps us understand how likely the cancer is to come back and whether chemotherapy would benefit you. Your score was 16, which is in the low range. This tells us the cancer has a lower chance of returning, and importantly, chemotherapy would only add about 1.6% benefit for someone your age with this score.
Patient: So I don't need chemotherapy?
Doctor: Based on this score, the benefit from chemotherapy is very small. However, I want to discuss the options with you so we can decide together. Let me explain what I recommend and why, and then I want to hear your thoughts.
Patient: Okay.
Doctor: The standard treatment plan I recommend includes three parts. First, you've already had the surgery, and we've completed radiation therapy to your chest wall, which reduces the risk of the cancer coming back in that area. Second, because your cancer is hormone receptor positive, I strongly recommend hormone therapy, a medication called tamoxifen, which you would take daily for five to ten years. This significantly reduces the risk of recurrence. Third, regarding chemotherapy, given your low Oncotype score, I don't think the small benefit outweighs the side effects for you. But I want to know how you feel about this.
Patient: I was dreading chemotherapy. If it's not going to help much, I'd rather not do it. But I'm worried about making the wrong choice.
Doctor: That's completely understandable. Let me put some numbers to this. Without any additional treatment after surgery and radiation, there's roughly a 15% chance of the cancer returning over the next ten years. With hormone therapy alone, that drops to about 7-8%. Adding chemotherapy might reduce it by another 1-2%. So you'd be going through significant side effects for a relatively small additional benefit. Does that help clarify things?
Patient: Yes, it does. I think I'll skip the chemotherapy but definitely do the hormone therapy.
Doctor: I think that's a reasonable decision, Maria. Now, let me address your question about family history. We did genetic testing on your tumor, and it did not show any of the known genetic mutations we look for, including BRCA1 and BRCA2. This is reassuring. However, given your family history of colorectal and hepatobiliary cancers, I would recommend you meet with a genetic counselor who can do a more comprehensive assessment and discuss what screening might be appropriate for your daughters when they're older.
Patient: That makes me feel better. Should my daughters be tested?
Doctor: Genetic testing is typically not done on children because there are no preventive interventions for them at a young age. But when they reach adulthood, around 25 to 30, they can make an informed decision about testing after meeting with a genetic counselor. For now, the most important thing is that you're here, you're getting treated, and you're going to be there for them.
Patient: Thank you for saying that.
Doctor: Now let me summarize what we've discussed. Your surgery successfully removed all the cancer with clear margins and negative lymph nodes. You've completed radiation. You'll start tamoxifen, which you'll take daily, and we've decided together that chemotherapy isn't necessary given your Oncotype score. You'll also meet with a genetic counselor about your family history. Do you have any questions about any of this?
Patient: How often will I need to come back for checkups?
Doctor: Great question. I'll see you every three to four months for the first two years, then every six months for years three to five, then annually after that. You'll also have yearly mammograms on your remaining breast. Now, there are some things I need you to watch for between appointments. If you notice any new lumps anywhere, especially in your other breast, under your arms, or along your surgical scar, please call us right away. Also watch for persistent bone pain, unexplained shortness of breath, or any symptoms that concern you. What should you watch for?
Patient: New lumps, bone pain, or trouble breathing, and anything that worries me.
Doctor: Exactly right. Don't hesitate to call, even if it turns out to be nothing. It's always better to check. Is there anything else you'd like to ask me, Maria?
Patient: No, I think you've explained everything really well. Thank you for taking the time to go through all of this with me.
Doctor: You're very welcome. You've been through a lot, and you've handled it with real strength. I'll see you in three months, but remember, my nurse can always get me a message if you have concerns before then. Take care of yourself.

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

### Example 15

**Conversation:**
Doctor: Good afternoon, Mrs. Patterson. I'm Dr. Hernandez, the neurologist. I've been asked to see you because of the new symptoms you've been experiencing. Before we dive into the test results, I'd like to hear from you. Can you tell me in your own words what's been happening?
Patient: It's been a nightmare, honestly. For months I've felt terrible, no appetite, exhausted all the time, losing weight without trying. Then the back pain started, and now my legs feel weak and tingly. I've even had some accidents with my bladder, which is humiliating.
Doctor: I'm so sorry you've been going through all of this. It sounds incredibly difficult. Thank you for sharing that with me. Is there anything else that's been concerning you?
Patient: Yes. Nobody seems to know what's wrong with me. I've had test after test, and I still don't have answers. I'm scared it's something serious, like cancer.
Doctor: That fear makes complete sense, especially with everything you've been through. Is there anything else you'd like to discuss today?
Patient: I just want to know what's causing all this. And what can be done about it.
Doctor: I understand completely. Let me tell you how I'd like to approach our conversation. First, I'm going to ask you some more detailed questions about your symptoms to make sure I fully understand what you're experiencing. Then I'll explain what the tests have shown us so far. Finally, we'll talk about what happens next. Does that sound okay?
Patient: Yes, please.
Doctor: Let's start with your legs. When did you first notice the weakness?
Patient: About two weeks ago. At first I thought I was just tired, but then I started having trouble with stairs. Now I feel unsteady when I walk, like I might fall.
Doctor: And the numbness and tingling, where exactly do you feel that?
Patient: It started in my feet and has gradually moved up to about my knees. It's like pins and needles, but constant.
Doctor: What about the bladder problems, when did those start?
Patient: About a week ago. I can't always tell when I need to go, and sometimes I don't make it in time. I've also been constipated.
Doctor: I appreciate you telling me all of this, I know it's not easy to discuss. Now, can you tell me what you think might be causing these symptoms?
Patient: I don't know. I keep thinking about the bone lesions they found on the CT scan months ago. Could they be related? And the fact that they haven't found a cancer yet, that terrifies me. Like maybe it's hiding somewhere.
Doctor: Those are very reasonable thoughts. What worries you most about all of this?
Patient: That it's something that can't be treated. That I'm going to keep getting worse. I live alone, and the thought of not being able to walk or take care of myself is overwhelming.
Doctor: I hear you. Independence is so important, and the uncertainty must be incredibly hard to live with. What are you hoping we can accomplish?
Patient: I just want a diagnosis. And if there's something wrong, I want to know if it can be fixed.
Doctor: That's what we're working toward, and I want to share with you what we've learned so far. Can I do that now?
Patient: Yes, please.
Doctor: The MRI of your brain and spine showed something significant. There's abnormal enhancement, which means something is coating the membranes that surround your spinal cord and brainstem. This is called leptomeningeal involvement. Are you with me so far?
Patient: I think so. Something is affecting my spinal cord?
Doctor: Exactly. The covering around your spinal cord. This explains your leg weakness, the numbness and tingling, the bladder and bowel problems, and the balance issues. When this area is affected, all of those symptoms can occur because the nerves that control those functions travel through there.
Patient: What's causing it?
Doctor: We did a lumbar puncture, a spinal tap, to analyze the fluid around your spine. It showed elevated protein and white blood cells, which confirms there's something abnormal happening there. We're now running additional tests on that fluid to determine exactly what's causing it.
Patient: Is it cancer?
Doctor: I want to be honest with you. Given everything we're seeing, including the bone lesions, the lymph node findings, the weight loss, and now this spinal involvement, we are concerned about the possibility of a malignancy. However, we haven't confirmed that yet. The spinal fluid tests will help us get closer to an answer.
Patient: How long until we know?
Doctor: Some results will come back within a few days. Others, like specific cancer markers, may take up to a week. I know waiting is hard, but I want us to have accurate information before we make any treatment decisions.
Patient: What happens if it is cancer?
Doctor: If it turns out to be cancer that has spread to the leptomeninges, there are treatments available. They might include chemotherapy delivered directly into the spinal fluid, radiation therapy, or systemic treatments depending on the cancer type. The treatment plan would depend on what type of cancer it is and where it started.
Patient: Is it treatable?
Doctor: I won't mislead you, this type of involvement can be serious. But many patients do respond to treatment, and our goal would be to control the disease and maintain your quality of life and function. We would work closely with oncology, and you would have a whole team supporting you.
Patient: What about my symptoms right now? Will my legs get better?
Doctor: That depends on how quickly we can start treatment once we have a diagnosis, and how your body responds. Some patients see improvement, others stabilize, and some unfortunately continue to progress. I wish I could give you a definite answer, but I want to be truthful with you.
Patient: I appreciate your honesty.
Doctor: Let me summarize what we've discussed. You have symptoms affecting your legs, bladder, and balance that are being caused by something involving the covering of your spinal cord. The MRI and lumbar puncture confirm there's a problem there. We're waiting for specific test results to determine exactly what it is. While we wait, we'll manage your symptoms and monitor you closely in the hospital. Once we have a diagnosis, we'll develop a treatment plan together. Does that capture everything?
Patient: Yes, I think so.
Doctor: Now, there are some things I need you and the nursing staff to watch for. If you notice any sudden worsening of your leg weakness, if you develop any new symptoms like difficulty swallowing, changes in your vision, or severe headaches, please alert us immediately. These could indicate the condition is progressing and we may need to act quickly. Can you repeat back what to watch for?
Patient: Sudden weakness getting worse, trouble swallowing, vision changes, or bad headaches.
Doctor: Perfect. Is there anyone you'd like us to contact, family members who should be here with you or who should know what's going on?
Patient: My daughter. She lives about two hours away, but she'd want to know.
Doctor: We can absolutely help facilitate that conversation. Would you like me to be present when you tell her, or would you prefer to speak with her privately first?
Patient: Maybe you could speak with her after I do, just to explain the medical side?
Doctor: Of course. I'll make myself available for that. Is there anything else you'd like to ask me, anything I haven't explained clearly?
Patient: No, I think you've explained things better than anyone else has. Thank you for being straight with me.
Doctor: You deserve honesty and respect, especially at a time like this. I'll check on you tomorrow, and as soon as any test results come in, I'll come speak with you personally. You're not alone in this, Mrs. Patterson. We're going to figure this out together.

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

### Example 16

**Conversation:**
Doctor: Good afternoon, Mrs. Patterson. I'm Dr. Hernandez, the neurologist. I've been asked to see you because of the new symptoms you've been experiencing. Before we dive into the test results, I'd like to hear from you. Can you tell me in your own words what's been happening?
Patient: It's been a nightmare, honestly. For months I've felt terrible, no appetite, exhausted all the time, losing weight without trying. Then the back pain started, and now my legs feel weak and tingly. I've even had some accidents with my bladder, which is humiliating.
Doctor: I'm so sorry you've been going through all of this. It sounds incredibly difficult. Thank you for sharing that with me. Is there anything else that's been concerning you?
Patient: Yes. Nobody seems to know what's wrong with me. I've had test after test, and I still don't have answers. I'm scared it's something serious, like cancer.
Doctor: That fear makes complete sense, especially with everything you've been through. Is there anything else you'd like to discuss today?
Patient: I just want to know what's causing all this. And what can be done about it.
Doctor: I understand completely. Let me tell you how I'd like to approach our conversation. First, I'm going to ask you some more detailed questions about your symptoms to make sure I fully understand what you're experiencing. Then I'll explain what the tests have shown us so far. Finally, we'll talk about what happens next. Does that sound okay?
Patient: Yes, please.
Doctor: Let's start with your legs. When did you first notice the weakness?
Patient: About two weeks ago. At first I thought I was just tired, but then I started having trouble with stairs. Now I feel unsteady when I walk, like I might fall.
Doctor: And the numbness and tingling, where exactly do you feel that?
Patient: It started in my feet and has gradually moved up to about my knees. It's like pins and needles, but constant.
Doctor: What about the bladder problems, when did those start?
Patient: About a week ago. I can't always tell when I need to go, and sometimes I don't make it in time. I've also been constipated.
Doctor: I appreciate you telling me all of this, I know it's not easy to discuss. Now, can you tell me what you think might be causing these symptoms?
Patient: I don't know. I keep thinking about the bone lesions they found on the CT scan months ago. Could they be related? And the fact that they haven't found a cancer yet, that terrifies me. Like maybe it's hiding somewhere.
Doctor: Those are very reasonable thoughts. What worries you most about all of this?
Patient: That it's something that can't be treated. That I'm going to keep getting worse. I live alone, and the thought of not being able to walk or take care of myself is overwhelming.
Doctor: I hear you. Independence is so important, and the uncertainty must be incredibly hard to live with. What are you hoping we can accomplish?
Patient: I just want a diagnosis. And if there's something wrong, I want to know if it can be fixed.
Doctor: That's what we're working toward, and I want to share with you what we've learned so far. Can I do that now?
Patient: Yes, please.
Doctor: The MRI of your brain and spine showed something significant. There's abnormal enhancement, which means something is coating the membranes that surround your spinal cord and brainstem. This is called leptomeningeal involvement. Are you with me so far?
Patient: I think so. Something is affecting my spinal cord?
Doctor: Exactly. The covering around your spinal cord. This explains your leg weakness, the numbness and tingling, the bladder and bowel problems, and the balance issues. When this area is affected, all of those symptoms can occur because the nerves that control those functions travel through there.
Patient: What's causing it?
Doctor: We did a lumbar puncture, a spinal tap, to analyze the fluid around your spine. It showed elevated protein and white blood cells, which confirms there's something abnormal happening there. We're now running additional tests on that fluid to determine exactly what's causing it.
Patient: Is it cancer?
Doctor: I want to be honest with you. Given everything we're seeing, including the bone lesions, the lymph node findings, the weight loss, and now this spinal involvement, we are concerned about the possibility of a malignancy. However, we haven't confirmed that yet. The spinal fluid tests will help us get closer to an answer.
Patient: How long until we know?
Doctor: Some results will come back within a few days. Others, like specific cancer markers, may take up to a week. I know waiting is hard, but I want us to have accurate information before we make any treatment decisions.
Patient: What happens if it is cancer?
Doctor: If it turns out to be cancer that has spread to the leptomeninges, there are treatments available. They might include chemotherapy delivered directly into the spinal fluid, radiation therapy, or systemic treatments depending on the cancer type. The treatment plan would depend on what type of cancer it is and where it started.
Patient: Is it treatable?
Doctor: I won't mislead you, this type of involvement can be serious. But many patients do respond to treatment, and our goal would be to control the disease and maintain your quality of life and function. We would work closely with oncology, and you would have a whole team supporting you.
Patient: What about my symptoms right now? Will my legs get better?
Doctor: That depends on how quickly we can start treatment once we have a diagnosis, and how your body responds. Some patients see improvement, others stabilize, and some unfortunately continue to progress. I wish I could give you a definite answer, but I want to be truthful with you.
Patient: I appreciate your honesty.
Doctor: Let me summarize what we've discussed. You have symptoms affecting your legs, bladder, and balance that are being caused by something involving the covering of your spinal cord. The MRI and lumbar puncture confirm there's a problem there. We're waiting for specific test results to determine exactly what it is. While we wait, we'll manage your symptoms and monitor you closely in the hospital. Once we have a diagnosis, we'll develop a treatment plan together. Does that capture everything?
Patient: Yes, I think so.
Doctor: Now, there are some things I need you and the nursing staff to watch for. If you notice any sudden worsening of your leg weakness, if you develop any new symptoms like difficulty swallowing, changes in your vision, or severe headaches, please alert us immediately. These could indicate the condition is progressing and we may need to act quickly. Can you repeat back what to watch for?
Patient: Sudden weakness getting worse, trouble swallowing, vision changes, or bad headaches.
Doctor: Perfect. Is there anyone you'd like us to contact, family members who should be here with you or who should know what's going on?
Patient: My daughter. She lives about two hours away, but she'd want to know.
Doctor: We can absolutely help facilitate that conversation. Would you like me to be present when you tell her, or would you prefer to speak with her privately first?
Patient: Maybe you could speak with her after I do, just to explain the medical side?
Doctor: Of course. I'll make myself available for that. Is there anything else you'd like to ask me, anything I haven't explained clearly?
Patient: No, I think you've explained things better than anyone else has. Thank you for being straight with me.
Doctor: You deserve honesty and respect, especially at a time like this. I'll check on you tomorrow, and as soon as any test results come in, I'll come speak with you personally. You're not alone in this, Mrs. Patterson. We're going to figure this out together.

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
