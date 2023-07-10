var symptoms = ['Abdomen, Acute', 'Abdominal Pain', 'Acute Coronary Syndrome', 'Aerophagy', 'Ageusia', 'Aging, Premature',
    'Agnosia', 'Akathisia, Drug-Induced', 'Albuminuria', 'Alexia, Pure', 'Amaurosis Fugax', 'Amblyopia', 'Amnesia', 'Amnesia, Anterograde',
    'Amnesia, Retrograde', 'Amnesia, Transient Global', 'Angina Pectoris', 'Angina Pectoris, Variant', 'Angina, Unstable', 'Anisocoria',
    'Anomia', 'Anorexia', 'Anoxia', 'Aphasia', 'Aphasia, Broca', 'Aphasia, Wernicke', 'Aphonia', 'Apnea', 'Apraxia, Ideomotor', 'Apraxias',
    'Arthralgia', 'Articulation Disorders', 'Asthenia', 'Ataxia', 'Athetosis', 'Auditory Perceptual Disorders', 'Back Pain', 'Birth Weight',
    'Blindness', 'Blindness, Cortical', 'Body Weight', 'Body Weight Changes', 'Brown-Sequard Syndrome', 'Bulimia', 'Cachexia', 'Cafe-au-Lait Spots',
    'Cardiac Output, High', 'Cardiac Output, Low', 'Catalepsy', 'Catatonia', 'Cerebellar Ataxia', 'Cerebrospinal Fluid Otorrhea',
    'Cerebrospinal Fluid Rhinorrhea', 'Chest Pain', 'Cheyne-Stokes Respiration', 'Chills', 'Chorea', 'Colic', 'Color Vision Defects', 'Coma',
    'Communication Disorders', 'Confusion', 'Consciousness Disorders', 'Constipation', 'Coprophagia', 'Cough', 'Cyanosis', 'Deafness',
    'Decerebrate State', 'Delirium', 'Diarrhea', 'Diarrhea, Infantile', 'Diplopia', 'Dizziness', 'Dysarthria', 'Dysgeusia', 'Dyskinesias', 'Dyslexia',
    'Dyslexia, Acquired', 'Dysmenorrhea', 'Dyspepsia', 'Dysphonia', 'Dyspnea', 'Dyspnea, Paroxysmal', 'Dystonia', 'Dysuria', 'Earache', 'Ecchymosis',
    'Edema', 'Edema, Cardiac', 'Emaciation', 'Encopresis', 'Eructation', 'Eye Hemorrhage', 'Eye Manifestations', 'Eye Pain', 'Facial Pain',
    'Facial Paralysis', 'Fasciculation', 'Fatigue', 'Feminization', 'Fetal Distress', 'Fetal Hypoxia', 'Fetal Macrosomia', 'Fetal Weight', 'Fever',
    'Fever of Unknown Origin', 'Flank Pain', 'Flatulence', 'Flushing', 'Gagging', 'Gait Apraxia', 'Gait Ataxia', 'Gait Disorders, Neurologic',
    'Gastroparesis', 'Glossalgia', 'Halitosis', 'Hallucinations', 'Headache', 'Hearing Disorders', 'Hearing Loss', 'Hearing Loss, Bilateral',
    'Hearing Loss, Central', 'Hearing Loss, Conductive', 'Hearing Loss, Functional', 'Hearing Loss, High-Frequency',
    'Hearing Loss, Mixed Conductive-Sensorineural', 'Hearing Loss, Noise-Induced', 'Hearing Loss, Sensorineural', 'Hearing Loss, Sudden',
    'Hearing Loss, Unilateral', 'Heart Murmurs', 'Heartburn', 'Hematemesis', 'Hemianopsia', 'Hemifacial Spasm', 'Hemiplegia', 'Hemoglobinuria',
    'Hemoptysis', 'Hiccup', 'Hirsutism', 'Hoarseness', 'Horner Syndrome', 'Hot Flashes', 'Hydrops Fetalis', 'Hyperalgesia', 'Hypercalciuria',
    'Hypercapnia', 'Hyperemesis Gravidarum', 'Hyperesthesia', 'Hypergammaglobulinemia', 'Hyperkinesis', 'Hyperoxia', 'Hyperphagia', 'Hyperventilation',
    'Hypesthesia', 'Hypocapnia', 'Hypokinesia', 'Hypothermia', 'Hypoventilation', 'Illusions', 'Intermittent Claudication', 'Jaundice', 'Jaundice, Obstructive',
    'Labor Pain', 'Language Development Disorders', 'Language Disorders', 'Learning Disorders', 'Lethargy', 'Livedo Reticularis', 'Low Back Pain',
    'Memory Disorders', 'Meningism', 'Mental Fatigue', 'Mental Retardation', 'Metatarsalgia', 'Miosis', 'Mobility Limitation', 'Motion Sickness',
    'Mouth Breathing', 'Muscle Cramp', 'Muscle Hypertonia', 'Muscle Hypotonia', 'Muscle Rigidity', 'Muscle Spasticity', 'Muscle Weakness', 'Muscular Atrophy',
    'Mutism', 'Myoclonus', 'Myokymia', 'Myotonia', 'Nausea', 'Neck Pain', 'Necrolytic Migratory Erythema', 'Neuralgia', 'Neuralgia, Postherpetic',
    'Neurobehavioral Manifestations', 'Neurologic Manifestations', 'Nocturia', 'Obesity', 'Obesity, Morbid', 'Olfaction Disorders', 'Oliguria',
    'Ophthalmoplegia', 'Ophthalmoplegia, Chronic Progressive External', 'Oral Hemorrhage', 'Oral Manifestations', 'Orthostatic Intolerance', 'Overweight',
    'Pain', 'Pain, Intractable', 'Pain, Postoperative', 'Pain, Referred', 'Pallor', 'Paralysis', 'Paraparesis', 'Paraparesis, Spastic', 'Paraplegia',
    'Paresis', 'Paresthesia', 'Pelvic Pain', 'Perceptual Disorders', 'Persistent Vegetative State', 'Phantom Limb', 'Photophobia', 'Polyuria',
    'Postoperative Nausea and Vomiting', 'Presbycusis', 'Prostatism', 'Proteinuria', 'Pruritus', 'Pseudobulbar Palsy', 'Pseudophakia', 'Psychomotor Agitation',
    'Psychomotor Disorders', 'Psychophysiologic Disorders', 'Pupil Disorders', 'Purpura', 'Purpura Fulminans', 'Purpura, Hyperglobulinemic',
    'Purpura, Schoenlein-Henoch', 'Purpura, Thrombocytopenic', 'Purpura, Thrombocytopenic, Idiopathic', 'Purpura, Thrombotic Thrombocytopenic', 'Quadriplegia',
    'Reflex, Abnormal', 'Reflex, Babinski', 'Renal Colic', 'Respiratory Aspiration', 'Respiratory Paralysis', 'Respiratory Sounds', 'Reticulocytosis',
    'Sarcopenia', 'Sciatica', 'Scotoma', 'Seizures', 'Sensation Disorders', 'Shoulder Pain', 'Skin Manifestations', 'Sleep Deprivation', 'Sleep Disorders',
    'Sneezing', 'Snoring', 'Somatosensory Disorders', 'Space Motion Sickness', 'Spasm', 'Speech Disorders', 'Stupor', 'Stuttering', 'Supranuclear Palsy, Progressive',
    'Sweating Sickness', 'Syncope', 'Syncope, Vasovagal', 'Synkinesis', 'Systolic Murmurs', 'Taste Disorders', 'Tetany', 'Thinness', 'Tics', 'Tinea Pedis',
    'Tinnitus', 'Tonic Pupil', 'Toothache', 'Torticollis', 'Tremor', 'Trismus', 'Unconsciousness', 'Urinary Bladder, Neurogenic', 'Urinary Bladder, Overactive',
    'Urinary Incontinence', 'Urinary Incontinence, Stress', 'Urinary Incontinence, Urge', 'Urinoma', 'Usher Syndromes', 'Vertigo', 'Virilism', 'Vision Disorders',
    'Vision, Low', 'Vocal Cord Paralysis', 'Voice Disorders', 'Vomiting', 'Vomiting, Anticipatory', 'Waterhouse-Friderichsen Syndrome', 'Weight Gain', 'Weight Loss'];

var exampleSymptoms = [
    ['Dyspnea', 'Respiratory Aspiration', 'Respiratory Sounds', 'Cough', 'Anoxia'],
    ['Back Pain', 'Hypercalciuria', 'Hypokinesia', 'Mobility Limitation', 'Muscle Spasticity', 'Muscle Weakness', 'Tetany']
];

var exampleSymptomIntensities = [
    [1, 4, 3, 2, 2],
    [6, 8, 5, 3, 4, 2, 2]
];

function getHTML() {
    var checkboxHTML = '<td style="width:10%;"><input type="checkbox" /></td>';
    var keyHTML = '<td style="width:70%;"><select class="full">';
    for (var i=0; i<symptoms.length; ++i)
        keyHTML += '<option value="' + symptoms[i] + '">' + symptoms[i] + '</option>';
    keyHTML += '</select></td>';
    var valueHTML = '<td style="width:20%;"><input type="number" min="0" max="10" step="0.01" class="full" placeholder="Enter symptom intensity (1-10)" required /></td>';
    return checkboxHTML + keyHTML + valueHTML;
}

function nameRows() {
    var allRows = document.getElementsByClassName('input_row');

    allRows[0].children[2].firstElementChild.name = 'v0';
    allRows[0].children[2].firstElementChild.id = 'v0';

    for(var i=1; i<allRows.length; ++i) {
        var row = allRows[i];
        //var input = row.childNodes[j].firstChild;
        row.children[0].firstElementChild.name = 'c' + i;
        row.children[1].firstElementChild.name = 'k' + i;
        row.children[2].firstElementChild.name = 'v' + i;

        row.children[0].firstElementChild.id = 'c' + i;
        row.children[1].firstElementChild.id = 'k' + i;
        row.children[2].firstElementChild.id = 'v' + i;
    }
}

function addRow() {
    var tableElement = document.getElementById('form_input_table');
    var rowElement = document.createElement("tr");
    rowElement.innerHTML = getHTML();
    rowElement.classList.add('input_row');
    tableElement.firstElementChild.appendChild(rowElement);

    (document.getElementById('total_count').value)++;
    nameRows();

}

function deleteRow() {
    var allRows = document.getElementsByClassName('input_row');
    var selectedRows = [];

    for(var i=1; i<allRows.length; ++i)
        if(allRows[i].firstChild.firstChild.checked == true)
            selectedRows.push(allRows[i]);

    for(var i=0; i<selectedRows.length; ++i) {
        document.getElementById('form_input_table').firstElementChild.removeChild(selectedRows[i]);
        (document.getElementById('total_count').value)--;
    }
    nameRows();
}

function deleteAllRows() {
    var allRows = document.getElementsByClassName('input_row');
    var nRows = allRows.length;
    for(var i=1; i<nRows; ++i) {
        document.getElementById('form_input_table').firstElementChild.removeChild(allRows[1]);
        (document.getElementById('total_count').value)--;
    }
}

function addExampleRows(index) {
    var symptoms = exampleSymptoms[index];
    var intensities = exampleSymptomIntensities[index];
    deleteAllRows();
    for(var i=1; i<symptoms.length; ++i)
        addRow();
    for(var i=0; i<symptoms.length; ++i) {
        document.getElementById('k' + i).value = symptoms[i];
        document.getElementById('v' + i).value = intensities[i];
    }
}
