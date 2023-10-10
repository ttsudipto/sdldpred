<?php
    $symptoms = array("Abdomen, Acute", "Abdominal Pain", "Acute Coronary Syndrome", "Aerophagy", "Ageusia", "Aging, Premature",
    "Agnosia", "Akathisia, Drug-Induced", "Albuminuria", "Alexia, Pure", "Amaurosis Fugax", "Amblyopia", "Amnesia", "Amnesia, Anterograde",
    "Amnesia, Retrograde", "Amnesia, Transient Global", "Angina Pectoris", "Angina Pectoris, Variant", "Angina, Unstable", "Anisocoria",
    "Anomia", "Anorexia", "Anoxia", "Aphasia", "Aphasia, Broca", "Aphasia, Wernicke", "Aphonia", "Apnea", "Apraxia, Ideomotor", "Apraxias",
    "Arthralgia", "Articulation Disorders", "Asthenia", "Ataxia", "Athetosis", "Auditory Perceptual Disorders", "Back Pain", "Birth Weight",
    "Blindness", "Blindness, Cortical", "Body Weight", "Body Weight Changes", "Brown-Sequard Syndrome", "Bulimia", "Cachexia", "Cafe-au-Lait Spots",
    "Cardiac Output, High", "Cardiac Output, Low", "Catalepsy", "Catatonia", "Cerebellar Ataxia", "Cerebrospinal Fluid Otorrhea",
    "Cerebrospinal Fluid Rhinorrhea", "Chest Pain", "Cheyne-Stokes Respiration", "Chills", "Chorea", "Colic", "Color Vision Defects", "Coma",
    "Communication Disorders", "Confusion", "Consciousness Disorders", "Constipation", "Coprophagia", "Cough", "Cyanosis", "Deafness",
    "Decerebrate State", "Delirium", "Diarrhea", "Diarrhea, Infantile", "Diplopia", "Dizziness", "Dysarthria", "Dysgeusia", "Dyskinesias", "Dyslexia",
    "Dyslexia, Acquired", "Dysmenorrhea", "Dyspepsia", "Dysphonia", "Dyspnea", "Dyspnea, Paroxysmal", "Dystonia", "Dysuria", "Earache", "Ecchymosis",
    "Edema", "Edema, Cardiac", "Emaciation", "Encopresis", "Eructation", "Eye Hemorrhage", "Eye Manifestations", "Eye Pain", "Facial Pain",
    "Facial Paralysis", "Fasciculation", "Fatigue", "Feminization", "Fetal Distress", "Fetal Hypoxia", "Fetal Macrosomia", "Fetal Weight", "Fever",
    "Fever of Unknown Origin", "Flank Pain", "Flatulence", "Flushing", "Gagging", "Gait Apraxia", "Gait Ataxia", "Gait Disorders, Neurologic",
    "Gastroparesis", "Glossalgia", "Halitosis", "Hallucinations", "Headache", "Hearing Disorders", "Hearing Loss", "Hearing Loss, Bilateral",
    "Hearing Loss, Central", "Hearing Loss, Conductive", "Hearing Loss, Functional", "Hearing Loss, High-Frequency",
    "Hearing Loss, Mixed Conductive-Sensorineural", "Hearing Loss, Noise-Induced", "Hearing Loss, Sensorineural", "Hearing Loss, Sudden",
    "Hearing Loss, Unilateral", "Heart Murmurs", "Heartburn", "Hematemesis", "Hemianopsia", "Hemifacial Spasm", "Hemiplegia", "Hemoglobinuria",
    "Hemoptysis", "Hiccup", "Hirsutism", "Hoarseness", "Horner Syndrome", "Hot Flashes", "Hydrops Fetalis", "Hyperalgesia", "Hypercalciuria",
    "Hypercapnia", "Hyperemesis Gravidarum", "Hyperesthesia", "Hypergammaglobulinemia", "Hyperkinesis", "Hyperoxia", "Hyperphagia", "Hyperventilation",
    "Hypesthesia", "Hypocapnia", "Hypokinesia", "Hypothermia", "Hypoventilation", "Illusions", "Intermittent Claudication", "Jaundice", "Jaundice, Obstructive",
    "Labor Pain", "Language Development Disorders", "Language Disorders", "Learning Disorders", "Lethargy", "Livedo Reticularis", "Low Back Pain",
    "Memory Disorders", "Meningism", "Mental Fatigue", "Mental Retardation", "Metatarsalgia", "Miosis", "Mobility Limitation", "Motion Sickness",
    "Mouth Breathing", "Muscle Cramp", "Muscle Hypertonia", "Muscle Hypotonia", "Muscle Rigidity", "Muscle Spasticity", "Muscle Weakness", "Muscular Atrophy",
    "Mutism", "Myoclonus", "Myokymia", "Myotonia", "Nausea", "Neck Pain", "Necrolytic Migratory Erythema", "Neuralgia", "Neuralgia, Postherpetic",
    "Neurobehavioral Manifestations", "Neurologic Manifestations", "Nocturia", "Obesity", "Obesity, Morbid", "Olfaction Disorders", "Oliguria",
    "Ophthalmoplegia", "Ophthalmoplegia, Chronic Progressive External", "Oral Hemorrhage", "Oral Manifestations", "Orthostatic Intolerance", "Overweight",
    "Pain", "Pain, Intractable", "Pain, Postoperative", "Pain, Referred", "Pallor", "Paralysis", "Paraparesis", "Paraparesis, Spastic", "Paraplegia",
    "Paresis", "Paresthesia", "Pelvic Pain", "Perceptual Disorders", "Persistent Vegetative State", "Phantom Limb", "Photophobia", "Polyuria",
    "Postoperative Nausea and Vomiting", "Presbycusis", "Prostatism", "Proteinuria", "Pruritus", "Pseudobulbar Palsy", "Pseudophakia", "Psychomotor Agitation",
    "Psychomotor Disorders", "Psychophysiologic Disorders", "Pupil Disorders", "Purpura", "Purpura Fulminans", "Purpura, Hyperglobulinemic",
    "Purpura, Schoenlein-Henoch", "Purpura, Thrombocytopenic", "Purpura, Thrombocytopenic, Idiopathic", "Purpura, Thrombotic Thrombocytopenic", "Quadriplegia",
    "Reflex, Abnormal", "Reflex, Babinski", "Renal Colic", "Respiratory Aspiration", "Respiratory Paralysis", "Respiratory Sounds", "Reticulocytosis",
    "Sarcopenia", "Sciatica", "Scotoma", "Seizures", "Sensation Disorders", "Shoulder Pain", "Skin Manifestations", "Sleep Deprivation", "Sleep Disorders",
    "Sneezing", "Snoring", "Somatosensory Disorders", "Space Motion Sickness", "Spasm", "Speech Disorders", "Stupor", "Stuttering", "Supranuclear Palsy, Progressive",
    "Sweating Sickness", "Syncope", "Syncope, Vasovagal", "Synkinesis", "Systolic Murmurs", "Taste Disorders", "Tetany", "Thinness", "Tics", "Tinea Pedis",
    "Tinnitus", "Tonic Pupil", "Toothache", "Torticollis", "Tremor", "Trismus", "Unconsciousness", "Urinary Bladder, Neurogenic", "Urinary Bladder, Overactive",
    "Urinary Incontinence", "Urinary Incontinence, Stress", "Urinary Incontinence, Urge", "Urinoma", "Usher Syndromes", "Vertigo", "Virilism", "Vision Disorders",
    "Vision, Low", "Vocal Cord Paralysis", "Voice Disorders", "Vomiting", "Vomiting, Anticipatory", "Waterhouse-Friderichsen Syndrome", "Weight Gain", "Weight Loss");

    function assertKey($key) {
        global $symptoms;
        return array_search($key, $symptoms);
    }

    function assertValue($val) {
        return is_numeric($val) && intval($val) >= 0 && intval($val) <= 10;
    }

    function validate($n, &$input_data) {
        for($i = 0; $i < $n; ++$i){
            $key = $_POST["k".strval($i)];
            $val = $_POST["v".strval($i)];
//             echo $key.",".assertKey($key)."<br/>";
//             echo $val.",".assertValue($val)."<br/>";
            if(assertKey($key) !== false && assertValue($val)) {
                $input_data[$key] = intval($val);
            } else {
                return false;
            }
        }
        return true;
    }

    function getDiseaseAssociations($symptoms) {
        $associations = array();
        $f = fopen("input/HSDN/pulmonary_symptom_disease_association_hsdn.tsv", "r");
        while (($data = fgetcsv($f, 0, "\t")) !== false) {
            if (array_search($data[1], $symptoms) !== false) {
                if (array_key_exists($data[1], $associations))
                    array_push($associations[$data[1]], /*$data[2]."-".*/$data[3]);
                else
                    $associations[$data[1]] = array(/*$data[2]."-".*/$data[3]);
            }
        }
        fclose($f);
//         foreach($associations as $s=>$a)
//             echo $s." => ".implode(", ", $a)."<br/><br/>";
        return $associations;
    }

    function getDrugHyperlinks($drugs) {
        $links = array();
        $f = fopen("input/CTD/pulmonary_drugs_ctd.tsv", "r");
        while (($data = fgetcsv($f, 0, "\t")) !== false) {
            $links[$data[2]] = $data[1];
        }
        fclose($f);
//         foreach($links as $d=>$link)
//             echo $d." => ".$link."<br/>";
        return $links;
    }


    $input_data = array();
    $symptom_count = $_POST["total_count"];
    validate($symptom_count, $input_data);
    $input_json = json_encode($input_data);
//     echo $input_json;

    $command = "venv/bin/python -m python.web_driver.driver '".$input_json."' 2>&1";
//     echo "<pre>".$command."</pre>\n";
    exec($command, $out, $status);
//     echo implode("</br/>", $out)."<br/>";  // for checking output with python errors, if any
//     echo $out[0]."<br/>";  // for checking output only
    $result = json_decode($out[0]);
//     print_r($result);
//     echo $result->estimator_id."<br/>";
//     echo implode("; ", $result->drugs)."<br/>";
//     echo implode("; ", $result->distances)."<br/>";
//     echo json_encode($result->associations)."<br/>";

    $drugHyperlinks = getDrugHyperlinks($result->drugs);
//     $associations = getDiseaseAssociations(array_keys($input_data));

?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Prediction - SDLDpred</title>
        <link rel = "stylesheet" type = "text/css" href = "css/main.css" />
        <script type = "text/javascript" src = "js/plot_density.js"></script>
        <script type = "text/javascript" src = "js/plot_heatmap.js"></script>
        <script type = "text/javascript" src = "https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body{
                background-color: #ffffff;
            }
        </style>
    </head>
    <body>
        <div class = "section_header">
            <center><p class="title">SDLDpred - Symptom-based Drugs of Lifestyle-related Diseases prediction</p></center>
        </div>

        <div class = "section_menu">
            <center>
            <table cellpadding="3px">
                <tr class="nav">
                    <td class="nav"><a href="index.html" class="side_nav">Home</a></td>
                    <td class="nav"><a href="about.html" class="side_nav">About</a></td>
                    <td class="nav"><a href="help.html" class="side_nav">Help</a></td>
                    <td class="nav"><a href="team.html" class="side_nav">Team</a></td>
                </tr>
            </table>
            </center>
        </div>

        <!--<div class = "section_left"></div>-->

        <div class = "section_middle">
            <h2>1. Drug prediction result</h2>
            <table class = "details" border = "0" cellpadding = "5px" id = "rtable">
                <tr>
                    <th>Predicted drugs</th>
                    <th>Euclidean distance</th>
                    <th>Confidence score (%)</th>
                </tr>
                <?php
                    $n_drugs = count($result->drugs);
                    for ($i = 0; $i < $n_drugs; ++$i){
                        echo "<tr>";
                        echo "<td><a style=\"color:blue;\" target=\"_blank\" href=\"https://ctdbase.org/detail.go?type=chem&acc=".$drugHyperlinks[$result->drugs[$i]]."\">".$result->drugs[$i]."</a></td>";
                        echo "<td>".strval($result->distances[$i])."</td>";
                        echo "<td>".strval($result->confidences[$i])."</td>";
                        echo "</tr>";
                    }
                ?>
            </table>
            <p style="width:80%; margin:0 10% 0 10%;">
                N.B. - The confidence score is the probability that the euclidean
                distance of the predicted drug is less than the euclidean distance
                between any two drugs.
            </p>
            <div id="plot_container_1" style="width:70%; margin:20px 15% 0 15%;"></div>
            <p style="width:70%; margin:10px 15% 0 15%;">
                N.B. - The grey region shows the euclidean distance range of 0 - 1.63
                for which the confidence score &gt; 90%.
            </p>

            <h2>2. Comparison of input symptoms with the symptom-associations of predicted drugs</h2>
            <div id="plot_container_2" style="width:100%; margin:0 0 0 0;"></div>

            <!--<h3>3. Disease associations of the input symptoms</h3>
            <table class = "summary" border = "0" cellpadding = "5px">
                <tr>
                    <th>Symptoms</th>
                    <th>Disease associations</th>
                </tr>
                <?php
//                     foreach($associations as $symptom=>$diseases) {
//                         echo "<tr><td>".$symptom."</td>";
//                         echo "<td>".implode("; ", $diseases)."</td></tr>";
//                     }
                ?>
            </table>-->
            <br/>
        </div>
        <?php
            $dist_arg_string = "[" . implode(",", $result->distances) . "]";
            $quoted_drug_strings = array();
            foreach($result->drugs as $d)
                array_push($quoted_drug_strings, "\"".$d."\"");
            $drugs_arg_string = "[" . implode(",", $quoted_drug_strings) . "]";
            echo "<script>plotDensity('plot_container_1', ".$dist_arg_string.", ".$drugs_arg_string.")</script>";

            echo "<script>plotHeatmap('plot_container_2', '".str_replace("'", "\\'", $out[0])."')</script>";
        ?>

        <br/><hr/>
        <p style="font-size:0.8em;text-align:center;">
            Please contact Dr. Sudipto Saha (<a href="mailto:ssaha4@jcbose.ac.in">ssaha4@jcbose.ac.in</a>,
            <a href="mailto:ssaha4@gmail.com">ssaha4@gmail.com</a>) regarding any further queries.
        </p>
    </body>
</html>

