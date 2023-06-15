from typing import List
from json import JSONEncoder
from copy import deepcopy
import numpy as np

symptoms = [
    'Abdomen, Acute', 'Abdominal Pain', 'Acute Coronary Syndrome', 'Aerophagy', 'Ageusia', 'Aging, Premature',
    'Agnosia', 'Akathisia, Drug-Induced', 'Albuminuria', 'Alexia, Pure', 'Amaurosis Fugax', 'Amblyopia', 'Amnesia',
    'Amnesia, Anterograde', 'Amnesia, Retrograde', 'Amnesia, Transient Global', 'Angina Pectoris',
    'Angina Pectoris, Variant', 'Angina, Unstable', 'Anisocoria', 'Anomia', 'Anorexia', 'Anoxia', 'Aphasia',
    'Aphasia, Broca', 'Aphasia, Wernicke', 'Aphonia', 'Apnea', 'Apraxia, Ideomotor', 'Apraxias', 'Arthralgia',
    'Articulation Disorders', 'Asthenia', 'Ataxia', 'Athetosis', 'Auditory Perceptual Disorders', 'Back Pain',
    'Birth Weight', 'Blindness', 'Blindness, Cortical', 'Body Weight', 'Body Weight Changes', 'Brown-Sequard Syndrome',
    'Bulimia', 'Cachexia', 'Cafe-au-Lait Spots', 'Cardiac Output, High', 'Cardiac Output, Low', 'Catalepsy',
    'Catatonia', 'Cerebellar Ataxia', 'Cerebrospinal Fluid Otorrhea', 'Cerebrospinal Fluid Rhinorrhea', 'Chest Pain',
    'Cheyne-Stokes Respiration', 'Chills', 'Chorea', 'Colic', 'Color Vision Defects', 'Coma', 'Communication Disorders',
    'Confusion', 'Consciousness Disorders', 'Constipation', 'Coprophagia', 'Cough',  'Cyanosis', 'Deafness',
    'Decerebrate State', 'Delirium', 'Diarrhea', 'Diarrhea, Infantile', 'Diplopia',  'Dizziness', 'Dysarthria',
    'Dysgeusia', 'Dyskinesias', 'Dyslexia', 'Dyslexia, Acquired', 'Dysmenorrhea', 'Dyspepsia', 'Dysphonia', 'Dyspnea',
    'Dyspnea, Paroxysmal', 'Dystonia', 'Dysuria', 'Earache', 'Ecchymosis', 'Edema', 'Edema, Cardiac', 'Emaciation',
    'Encopresis', 'Eructation', 'Eye Hemorrhage', 'Eye Manifestations', 'Eye Pain', 'Facial Pain', 'Facial Paralysis',
    'Fasciculation', 'Fatigue', 'Feminization', 'Fetal Distress', 'Fetal Hypoxia', 'Fetal Macrosomia', 'Fetal Weight',
    'Fever', 'Fever of Unknown Origin', 'Flank Pain', 'Flatulence', 'Flushing', 'Gagging', 'Gait Apraxia',
    'Gait Ataxia', 'Gait Disorders, Neurologic', 'Gastroparesis', 'Glossalgia', 'Halitosis', 'Hallucinations',
    'Headache', 'Hearing Disorders', 'Hearing Loss', 'Hearing Loss, Bilateral',  'Hearing Loss, Central',
    'Hearing Loss, Conductive', 'Hearing Loss, Functional', 'Hearing Loss, High-Frequency',
    'Hearing Loss, Mixed Conductive-Sensorineural', 'Hearing Loss, Noise-Induced', 'Hearing Loss, Sensorineural',
    'Hearing Loss, Sudden', 'Hearing Loss, Unilateral', 'Heart Murmurs', 'Heartburn', 'Hematemesis', 'Hemianopsia',
    'Hemifacial Spasm', 'Hemiplegia', 'Hemoglobinuria', 'Hemoptysis', 'Hiccup', 'Hirsutism', 'Hoarseness',
    'Horner Syndrome', 'Hot Flashes', 'Hydrops Fetalis', 'Hyperalgesia', 'Hypercalciuria', 'Hypercapnia',
    'Hyperemesis Gravidarum', 'Hyperesthesia', 'Hypergammaglobulinemia', 'Hyperkinesis', 'Hyperoxia', 'Hyperphagia',
    'Hyperventilation', 'Hypesthesia', 'Hypocapnia', 'Hypokinesia', 'Hypothermia', 'Hypoventilation', 'Illusions',
    'Intermittent Claudication', 'Jaundice', 'Jaundice, Obstructive', 'Labor Pain', 'Language Development Disorders',
    'Language Disorders', 'Learning Disorders', 'Lethargy', 'Livedo Reticularis', 'Low Back Pain', 'Memory Disorders',
    'Meningism', 'Mental Fatigue', 'Mental Retardation', 'Metatarsalgia', 'Miosis', 'Mobility Limitation',
    'Motion Sickness', 'Mouth Breathing', 'Muscle Cramp', 'Muscle Hypertonia', 'Muscle Hypotonia', 'Muscle Rigidity',
    'Muscle Spasticity', 'Muscle Weakness', 'Muscular Atrophy', 'Mutism', 'Myoclonus', 'Myokymia', 'Myotonia', 'Nausea',
    'Neck Pain', 'Necrolytic Migratory Erythema', 'Neuralgia', 'Neuralgia, Postherpetic',
    'Neurobehavioral Manifestations', 'Neurologic Manifestations', 'Nocturia', 'Obesity', 'Obesity, Morbid',
    'Olfaction Disorders', 'Oliguria', 'Ophthalmoplegia', 'Ophthalmoplegia, Chronic Progressive External',
    'Oral Hemorrhage', 'Oral Manifestations', 'Orthostatic Intolerance', 'Overweight', 'Pain', 'Pain, Intractable',
    'Pain, Postoperative', 'Pain, Referred', 'Pallor', 'Paralysis', 'Paraparesis', 'Paraparesis, Spastic', 'Paraplegia',
    'Paresis', 'Paresthesia', 'Pelvic Pain', 'Perceptual Disorders', 'Persistent Vegetative State', 'Phantom Limb',
    'Photophobia', 'Polyuria', 'Postoperative Nausea and Vomiting', 'Presbycusis', 'Prostatism', 'Proteinuria',
    'Pruritus', 'Pseudobulbar Palsy', 'Pseudophakia', 'Psychomotor Agitation', 'Psychomotor Disorders',
    'Psychophysiologic Disorders', 'Pupil Disorders', 'Purpura', 'Purpura Fulminans', 'Purpura, Hyperglobulinemic',
    'Purpura, Schoenlein-Henoch', 'Purpura, Thrombocytopenic', 'Purpura, Thrombocytopenic, Idiopathic',
    'Purpura, Thrombotic Thrombocytopenic', 'Quadriplegia', 'Reflex, Abnormal', 'Reflex, Babinski', 'Renal Colic',
    'Respiratory Aspiration', 'Respiratory Paralysis', 'Respiratory Sounds', 'Reticulocytosis', 'Sarcopenia',
    'Sciatica', 'Scotoma', 'Seizures', 'Sensation Disorders', 'Shoulder Pain', 'Skin Manifestations',
    'Sleep Deprivation', 'Sleep Disorders', 'Sneezing', 'Snoring', 'Somatosensory Disorders', 'Space Motion Sickness',
    'Spasm', 'Speech Disorders', 'Stupor', 'Stuttering', 'Supranuclear Palsy, Progressive', 'Sweating Sickness',
    'Syncope', 'Syncope, Vasovagal', 'Synkinesis', 'Systolic Murmurs', 'Taste Disorders', 'Tetany', 'Thinness', 'Tics',
    'Tinea Pedis', 'Tinnitus', 'Tonic Pupil', 'Toothache', 'Torticollis', 'Tremor', 'Trismus', 'Unconsciousness',
    'Urinary Bladder, Neurogenic', 'Urinary Bladder, Overactive', 'Urinary Incontinence',
    'Urinary Incontinence, Stress', 'Urinary Incontinence, Urge', 'Urinoma', 'Usher Syndromes', 'Vertigo', 'Virilism',
    'Vision Disorders', 'Vision, Low', 'Vocal Cord Paralysis', 'Voice Disorders', 'Vomiting', 'Vomiting, Anticipatory',
    'Waterhouse-Friderichsen Syndrome', 'Weight Gain', 'Weight Loss']


class Input:
    def __init__(self) -> None:
        self.input_params = deepcopy(symptoms)
        self.input_values = []
        self.param_length = len(self.input_params)
        self.estimator_id = 'BKM'

    def add_param(self, param: str) -> None:
        self.input_params.append(param)

    def add_value(self, value: float) -> None:
        self.input_values.append(value)

    def set_estimator_id(self, e_id: str) -> None:
        self.estimator_id = e_id

    def get_estimator_id(self) -> str:
        return self.estimator_id

    def get_all_params(self) -> List[str]:
        return self.input_params

    def get_all_values(self) -> List[float]:
        return self.input_values

    def get_value(self, index: int) -> float:
        return self.input_values[index]

    def get_param(self, index: int) -> str:
        return self.input_params[index]

    def get_ndarray(self) -> np.array:
        return np.array(self.input_values, dtype=np.float32).reshape(1, -1)


class Output:
    def __init__(self, estimator_id: str) -> None:
        self.estimator_id = estimator_id
        self.drugs = []
        self.distances = []
        self.confidences = []
        self.associations = []

    def add_neighbor(self, drug: str, distance: float, confidence: float) -> None:
        self.drugs.append(drug)
        self.distances.append(distance)
        self.confidences.append(confidence)

    def add_association(self, association: List[float]) -> None:
        self.associations.append(association)


class OutputEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Output):
            out_dict = dict()
            out_dict['estimator_id'] = obj.estimator_id
            out_dict['drugs'] = obj.drugs
            out_dict['distances'] = obj.distances
            out_dict['confidences'] = obj.confidences
            out_dict['associations'] = obj.associations
            return out_dict
        return JSONEncoder.default(self, obj)
