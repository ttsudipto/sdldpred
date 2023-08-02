# SDLDpred - Symptom-based Drugs of Lifestyle-related Diseases prediction
**SDLDpred** is a web-based tool to predict drugs of lifestyle-related diseases
using symptoms as features. It uses an unsupervised machine learning model
trained using  *Bisecting K-Means* algorithm to perform the prediction. The
model was trained with  disease-symptom and drug-disease association data of
*143 lifestyle-related diseases*, *1271 drugs* and *305 symptoms*.

## Using the tool
SDLDpred is available at: http://bicresources.jcbose.ac.in/ssaha4/sdldpred.

To know more about SDLDpred, go to
[About](http://bicresources.jcbose.ac.in/ssaha4/sdldpred/about.html) page.
For help, please refer to
[Help](http://bicresources.jcbose.ac.in/ssaha4/sdldpred/help.html) page.
The datasets used to develop the ML models are also available in the
[About](http://bicresources.jcbose.ac.in/ssaha4/sdldpred/about.html) page.

## Development
Python libraries used for developing the ML models :

* numpy (Version-`1.24.1`)
* scikit-learn (Version-`1.2.1`)
* joblib (Version-`1.2.0`)
* scipy (Version-`1.10.0`)
* ssmpy (Version-`0.2.5`)

Plotly JS library was used to display plots in the web page.

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
