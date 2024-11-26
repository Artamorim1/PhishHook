# Phish Hook - Analyzing ML-based Phishing Detection  

This repository contains the code, datasets, and models for the Phish Hook group, comprised of Arthur Amorim, Aneka Williams, and Randy Marcelin, for their **CAP5150** project. Our work extends the phishing website detection research by Gangesh Basker and his team (I have listed them as contributors in the git hub, to highlight the files that i did not change and do not have authorship over), aiming to enhance phishing detection using machine learning models and feature extraction methods.  

## Background  

For detailed background information, please refer to the (insert our publication pdf) in this repository. This project primarily builds upon the original work available at [Gangesh Basker's GitHub Repository](https://github.com/gangeshbaskerr/Phishing-Website-Detection).  

### Overview of the Datasets  

- **Dataset 1**: The original dataset from Basker's work.  
- **Dataset 2 & Dataset 3**: These are key datasets referenced in our paper.  
- **Dataset 4**: Created as part of this project using the same methods described in the original work. The steps for creating this dataset include:  
  1. Using the benign dataset provided by the University of New Brunswick (`dataset-Benign-full.csv`).  
  2. Sampling 5000 random entries from the benign dataset.  
  3. Labeling phishing URLs as `1` and non-phishing URLs as `0`.  
  4. Merging the labeled URLs into a combined dataset of 10,000 URLs (`dataset4.csv`).  

### Extracted Features  

- The files prefixed with `extracted` (e.g., `extracted1.csv`, `extracted2.csv`, etc.) represent datasets with 17 extracted features as detailed in the original paper.  
- `extractedTest.csv` and other test files are preprocessed datasets for quick reproduction of our results.  

## How to Reproduce Results  

To reproduce the results discussed in our paper and create or test datasets, follow these steps:  

### Environment Setup  

1. **Clone the Repository**  
   ```bash  
   git clone https://github.com/Artamorim1/PhishHook.git  
   cd PhishHook  
   ```  

2. **Install Requirements**  
   Make sure you have Python installed (preferably Python 3.13 or later). Install the necessary packages:  
   ```bash  
   pip install -r requirements.txt  
   ```  

### Running the Code  

1. **Dataset Creation and Feature Extraction**  
   - Use the provided `features.py` scripts to extract features for specific datasets:  
     - `features2.py` for `dataset2.csv` → Outputs `extracted2.csv`.  
     - `features3.py` for `dataset3.csv` → Outputs `extracted3.csv`.  
     - Similarly, use corresponding scripts for other datasets.  

2. **Reproducing Dataset 4**  
   - Follow the instructions in [modeltesting.ipynb](modeltesting.ipynb) to recreate `dataset4.csv` and extract its features.  

3. **Testing Models**  
   - The Jupyter notebook [modeltesting.ipynb](modeltesting.ipynb) explains how to test our models against the extracted datasets (`extractedTest.csv` and others).  

### Notes on Models  

- `XGBoostClassifier.pickle.dat`: Original model from the previous research.  
- `XGBoostClassifier.json`: Updated model, repackaged for compatibility with current Python and XGBoost versions.  

## Repository Structure  

| File/Folder            | Description                                                                                 |  
|------------------------|---------------------------------------------------------------------------------------------|  
| `Phishing Website Detection.pdf` | Detailed paper for the Phish Hook project.                                          |  
| `modeltesting.ipynb`   | Jupyter notebook for creating Dataset 4 and reproducing model results.                      |  
| `dataset*.csv`         | Original and newly created datasets for phishing detection.                                 |  
| `extracted*.csv`       | Datasets with 17 extracted features.                                                       |  
| `features*.py`         | Python scripts for feature extraction from datasets.                                       |  
| `XGBoostClassifier.json` | Updated and repackaged XGBoost model.                                                     |  
| `mlp_model.pkl`        | Multi-Layer Perceptron (MLP) model for phishing detection.                                  |  
| `requirements.txt`     | Required Python dependencies.                                                              |  

## Additional Notes  

- All datasets and extracted datasets are stored in their respective folders for compactness. If you wish to run a specific script, move the required files to the main directory.  
- To avoid overwriting, compare your generated files with the provided ones in the repository.  

## Credits  

This project is part of the CAP5150 course at UCF, taught by Dr. Mohaisen. It was completed by Arthur Amorim, Aneka Williams, and Randy Marcelin, extending the work of Gangesh Basker and his team.  
