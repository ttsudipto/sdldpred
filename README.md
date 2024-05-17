# SDLDpred - Symptom-based Drugs of Lifestyle-related Diseases prediction

SDLDpred is a web-based tool to predict drugs of lifestyle-related diseases using symptoms
as features.

It uses an unsupervised machine learning model trained using Bisecting K-Means algorithm to
perform the prediction. The model was trained with *novel drug-symptom associations* computed
from the disease-symptom and drug-disease association data of *143 lifestyle-related diseases*, 
*1271 drugs* and *305 symptoms*.

 **Cite as:**

>Bhattacharjee, S., Saha, B., & Saha, S. (2024). Symptom-based drug prediction of
lifestyle-related chronic diseases using unsupervised machine learning techniques. *Computers
in Biology and Medicine*, 174, 108413.<br/>
[https://doi.org/10.1016/j.compbiomed.2024.108413](https://doi.org/10.1016/j.compbiomed.2024.108413).

## Using the tool

SDLDpred is available at: [http://bicresources.jcbose.ac.in/ssaha4/sdldpred](http://bicresources.jcbose.ac.in/ssaha4/sdldpred).

To know more about the datasets and the methodology, please refer to the 
[About](http://bicresources.jcbose.ac.in/ssaha4/pulmopred/about.html) page. Please refer to 
the [Help](http://bicresources.jcbose.ac.in/ssaha4/pulmopred/help.html) page for understanding 
the inputs and outputs to the web application.

## Development

Python libraries used :

* numpy (Version `1.24.1`)
* scikit-learn (Version `1.2.1`)
* joblib (Version `1.2.0`)
* scipy (Version `1.10.1`)
* ssmpy (Version `0.2.5`)

R libraries used :

* GOSemSim (Version `2.26.0`)
* clusterProfiler (Version `4.8.1`)
* fmcsR (Version `1.42.0`)
* ggplot2 (Version `3.4.2`)
* ggpubr (Version `0.6.0`)
* patchwork (Version `1.1.2`)
* pheatmap (Version `1.0.12`)

The web application is deployed in an Apache HTTP server.

## Team
* **Sudipto Bhattacharjee** *([ttsudipto@gmail.com](mailto:ttsudipto@gmail.com))*<br/>
  Ph.D. Scholar,<br/>
  Department of Computer Science and Engineering,<br/>
  University of Calcutta, Kolkata, India.<br/>
* **Dr. Banani Saha** *([bsaha_29@yahoo.com](mailto:bsaha_29@yahoo.com))*<br/>
  Associate Professor,<br/>
  Department of Computer Science and Engineering,<br/>
  University of Calcutta, Kolkata, India.
* **Dr. Sudipto Saha** *([ssaha4@jcbose.ac.in](mailto:ssaha4@jcbose.ac.in))*<br/>
  Associate Professor,<br/>
  Department of Biological Sciences,<br/>
  Bose Institute, Kolkata, India.
  
*Please contact Dr. Sudipto Saha regarding any further queries.*
