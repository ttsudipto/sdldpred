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

function findMaxLength(data) {
    var max = 0;
    for (var i=0; i<data.length; ++i) {
        if (data[i].length > max)
            max = data[i].length;
    }
    return max;
}

function makeHeatmapPlot(div_id, heatmapData) {
    var graphDiv = document.getElementById(div_id);
    var minHeight = 400;
    var computedHeight = (30*heatmapData.drugs.length + 500);
    var drugNames = heatmapData.drugs.reverse().concat(['** Input **']);
    var maxLengthDrugName = findMaxLength(drugNames);

    var data = [{
            x: symptoms,
            y: drugNames,
            z: heatmapData.associations.reverse(),
            xgap: 0,
            ygap: 0,
            zmin: 0,
            zmax: 1,
            colorscale: 'Greens',
            reversescale: true,
            colorbar: {
                len: 0.7,
                title: {
                    text: 'Drug-symptom association',
                    side: 'right',
                    font: {size: 16}
                }
            },
            type: 'heatmap'
        }];

    var layout = {
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: ((computedHeight < minHeight) ? minHeight : computedHeight),
//         height: 800,
        bargap: 10,
        margin: {
            t: 10,
            l: 100 + maxLengthDrugName * 3,
            b: 240
        },
        hoverlabel: {
            font: {size: 16}
        },
        xaxis: {
            visible : true,
            color: 'black',
            linewidth: 2,
            ticks: 'outside',
            ticklen: 10,
            tickwidth: 2,
            tickfont: {size: 10},
            title : {
                text : 'Symptoms',
                font: {size: 22}
            }
        },
        yaxis: {
            visible : true,
            color: 'black',
            linewidth: 2,
            ticks: 'outside',
            ticklen: 10,
            tickwidth: 2,
            tickfont: {size: 14},
            title : {
                text : 'Drugs',
                font: {size: 22}
            }
        }
    };

    Plotly.plot(graphDiv, data, layout, {showSendToCloud:false});
}

function plotHeatmap(div_id, response) {
    var data = JSON.parse(response);
    makeHeatmapPlot(div_id, data);
}
