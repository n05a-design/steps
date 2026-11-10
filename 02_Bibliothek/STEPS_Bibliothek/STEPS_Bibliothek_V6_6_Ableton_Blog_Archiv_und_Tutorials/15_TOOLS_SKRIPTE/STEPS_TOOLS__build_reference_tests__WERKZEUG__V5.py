import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
cases={
'notation':[
('F#4 / Gb4','equal sounding pc 6 in 12TET','same spelled note','V5-001'),
('C to E / C to Fb','major third vs diminished fourth despite equal 12TET span','same interval quality','V5-001'),
('German H vs international B','both represent pitch class 11 in common 12TET naming','German B is B natural','V5-001'),
('German B vs international Bb','both represent pitch class 10 in common 12TET naming','German B is identical to English B natural','V5-001'),
('C7(b9)','C E G Bb Db are canonical spelled chord tones','C# is the canonical flat ninth','V5-026'),
('Cmaj9 / C9','maj9 includes B, dominant 9 includes Bb','both imply same seventh','V5-026'),
('Csus4','suspension replaces third in basic chord symbol','E is obligatory in basic Csus4','V5-026'),
('Cadd9','D added to C major; seventh not implied','Bb always present','V5-026'),
('Gb major scale','Gb Ab Bb Cb Db Eb F','Gb Ab Bb B Db Eb F is correctly spelled diatonic','V5-001'),
('F# major scale','F# G# A# B C# D# E#','F# G# A# B C# D# F is correctly spelled diatonic','V5-001'),
('C# major scale','C# D# E# F# G# A# B#','C# D# F F# G# A# C is canonical spelling','V5-001'),
('C/E vs V/ii','slash bass syntax vs applied Roman numeral syntax','treat slash as one grammar','V5-010'),
],
'modal_and_minor':[
('Dm7 G7 Dm7 with D pedal','D-Dorian is plausible','must be ii-V in C','V5-001'),
('Dm7 G7 C major cadence','ii V I in C is plausible','must be D-Dorian','V5-001'),
('Em F Em with E tonic','Phrygian-context bII color plausible','must be a functional cadence in C','V5-001'),
('C Bb F C','Mixolydian-oriented I bVII IV I plausible','must be in F major','V5-001'),
('Am Dm E7 Am','G# in E7 is common minor dominant practice','A natural minor forbids G#','V5-001'),
('Am G F Em','E minor v is plausible in modal/pop minor','the v is automatically wrong','V5-001'),
('C D E F G A B','pitch collection cannot prove tonic','pitch collection necessarily C-Ionian','V5-001'),
('D E F G A B C','pitch collection cannot prove D-Dorian','every sample using these notes is D-Dorian','V5-001'),
('G7 C recurring vamp','chord pair alone does not prove cadence','every G7-C is perfect authentic cadence','V5-007'),
('Fmaj7 Fm6 C','iv mixture context possible','F minor chord always sad','V5-001'),
],
'harmony_and_progressions':[
('C A7 Dm','A7 is V7/ii in common C major reading','A7 entails modulation to D minor','V5-010'),
('C E7 Am','E7 is V7/vi in common C-major reading','E7 must mean E major is new tonic','V5-010'),
('C G7 Am','deceptive move is context dependent','V7-vi always marks end of phrase','V5-001'),
('G7 Db7 to C','tritone substitution is a possible jazz lens','Db7 is sounding-identical to G7','V5-026'),
('Db7 guides','Db7 contains F and Cb (enharmonic B)','Db7 is written F and B in standard tertian spelling','V5-026'),
('Cmaj7 Am7','C E G common tones in suitable voicing','exact same voiceleading regardless register','V5-015'),
('C E Ab C','chromatic-mediant explanation can be relevant','must be I V/vi bVI I in all contexts','V5-015'),
('C7 in 12-bar blues','I7 as tonic color is valid','C7 must be V7/IV','V5-007'),
('F7 in C blues','IV7 is blues-conventional','F7 is illegal in C blues','V5-007'),
('Am F C G','C-major vi IV I V and A-minor i VI III VII possible','key can be established without other context','V5-005'),
('Am F G G leading to C chorus','emergent tonic hypothesis possible','if C is absent in verse no C-center can be heard','V5-005'),
('Cmaj7 Fm6 C/E','potential A-Ab-G line if voiced','A-Ab-G automatically occurs in every voicing','V5-015'),
('C E7 Am','G# in E7 is leading tone to A','E7 has G natural in default spelling','V5-026'),
('Cmaj7 #11','F# can be extension #11','Gb is the canonical spelled #11','V5-026'),
],
'composing_and_form':[
('8 bars unspecified','eight bars alone do not establish sentence form','always sentence','V5-002'),
('4+4 with weak/strong endings','antecedent/consequent period hypothesis possible','all 4+4 blocks are periods','V5-002'),
('motif C D E augmentation','rhythmic durations scale while pitch order preserved','always invert pitch too','V5-001'),
('motif C D E chromatic inversion around C','C Bb Ab is one possible chromatic mirror','inversion is always unique without pivot','V5-001'),
('retrograde','reverses chosen ordered dimension','all retrogrades must reverse pitch and timing identically','V5-001'),
('theme and variation','motivic relation requires specified invariant/operation','different chords alone prove thematic variation','V5-002'),
('form Verse Prechorus Chorus','harmonic trajectory may culminate on chorus entrance','cadence must be last bar of chorus','V5-003'),
('no tonic until chorus','emergent tonic is one analytic hypothesis','tonic must sound each verse','V5-005'),
('new orchestration same harmony','timbral density and register matter for perception','same chords implies identical impression','V5-019'),
('cantus firmus species check','species rules apply under specified strict framework','species rules govern all musical styles','V5-001'),
('MIDI imported score','MIDI note PCs cannot recover unique enharmonic spelling','MIDI pitch 66 always notated F#','V5-024'),
('32-bar piece without phrase metadata','bar count does not determine form','always AABA','V5-003'),
],
'culture_and_corpus':[
('maqam pitch collection','maqam includes melodic course sayr and jins-related practice','maqam equals western scale rotation','V5-020'),
('Hindustani raga','raga includes performative and aesthetic aspects','raga equals chord progression','V5-021'),
('African rhythm generic label','avoid treating diverse practices as uniform','all African music has one rhythmic system','V5-022'),
('Rock corpus historical bias','genre sample and era distributions affect claims','all observed percentages are universal','V5-007'),
('ChoCo JAAH/CASD/Mozart subset','specific subsets have CC BY-NC-SA exception','all ChoCo CC BY 4.0 unrestricted','V5-011'),
('When in Rome converted analysis','derived analyses may retain original license','all source analysis files share one new license','V5-012'),
('music21 code corpus','BSD code does not imply unrestricted corpus','all encoded scores are BSD','V5-013'),
('publisher abstract source','metadata landing page is not full book review','can cite nonexistent page as read','V5-015'),
('DCML applied chord','relative slash relates to local context','every slash means a bass inversion','V5-010'),
('MIDI 2.0','extension to MIDI 1.0','MIDI 1.0 is universally obsolete','V5-025'),
('MusicXML 4.0','symbolic score exchange format','guarantees identical audio across apps','V5-024'),
('style-specific valid example','explain musical scope and alternate traditions','style categories are rigid universal correctness constraints','V5-022')
]
}
records=[]
for domain,entries in cases.items():
 for raw,accept,reject,ref in entries:
  records.append({'id':f'V5-CASE-{len(records)+1:03d}','domain':domain,'input_description':raw,'expected_assertion':accept,'forbidden_overclaim':reject,'evidence_ref':ref,'status':'manual_expected_behavior_design','automated_executable':False,'review_status':'pending'})
(ROOT/'CONCEPTUAL_GOLDEN_AND_NEGATIVE_CASES_V5.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
with (ROOT/'CONCEPTUAL_GOLDEN_AND_NEGATIVE_CASES_V5.md').open('w',encoding='utf8') as f:
 f.write('# Konzeptionelle Positiv-/Negativfälle für Codex V5\n\n')
 f.write('Diese Fälle sind **testbare Anforderungen an künftige Analyseantworten**, derzeit kein ausgeführter Algorithmustest. Erwartungsstatements stehen neben bewusst verbotenen Überbehauptungen. Der Bezug auf eine Quelle bedeutet thematische Forschungsbasis, nicht zwingend geprüfter Seitenbeleg für die exakte Formulierung.\n\n')
 for r in records:
  f.write(f"### {r['id']} – {r['input_description']}\n\n- **Akzeptieren:** {r['expected_assertion']}\n- **Nicht behaupten:** {r['forbidden_overclaim']}\n- **Forschungsanker:** {r['evidence_ref']} (Status im Quellenregister).\n- **Fachreview:** offen.\n\n")
print('conceptual cases',len(records))
