import os
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
import pandas as pd
import temoatools as tt

#=======================================================
# Function to evaluate a single model
#=======================================================
def evaluateMonteCarlo(modelInputs, scenarioXLSX, scenarioName, temoa_paths, cases, caseNum):  

    # Unique filename
    model_filename = scenarioName + '_MC_' + str(caseNum)
    
    # Prepare monte carlo inputs
    cols = ['type', 'variable', 'tech', caseNum]
    MCinputs = cases.ix[:,cols]
    MCinputs = MCinputs.rename(columns={caseNum:'multiplier'})
    
    # Build Model
    tt.build(modelInputs,scenarioXLSX,scenarioName,model_filename,MCinputs=MCinputs,path='data')

    # Run Model
    saveEXCEL=False
    tt.run(model_filename,temoa_paths,saveEXCEL=saveEXCEL)
    
    # Analyze Results
    folder = os.getcwd() + '\\Databases'
    db = model_filename + '.sqlite'
    yearlyCosts, LCOE = tt.getCosts(folder, db)
    yearlyEmissions, avgEmissions = tt.getEmissions(folder, db)
    
    # Package Outputs
    output = pd.Series()
    output['db']              = db
    output['caseNum']         = caseNum
    output['LCOE']            = LCOE
    output['avgEmissions']    = avgEmissions
    for ind in yearlyCosts.index:
        label = 'cost_' + str(ind)
        output[label] = yearlyCosts.loc[ind]
    for ind in yearlyEmissions.index:
        label = 'emis_' + str(ind)
        output[label] = yearlyEmissions.loc[ind]
    
    return output
    
if __name__ == '__main__':
    
    #=======================================================
    # Model Inputs
    #=======================================================
    modelInputs_XLSX        = 'data.xlsx'
    scenarioInputs          = 'scenarios.xlsx'
    scenarioNames           = ['A','B','C','D'] 
    paths                   = 'paths.csv'
    sensitivityInputs       = 'sensitivityVariables.xlsx'
    sensitivityMultiplier   = 10.0 # percent perturbation
    
    #=======================================================
    # Move modelInputs_XLSX to database
    #=======================================================
    modelInputs = tt.move_data_to_db(modelInputs_XLSX, path='data')
    
    #=======================================================
    # Create directory to hold inputs and outputs
    #=======================================================
    workDir = os.getcwd()
    sensDir = workDir + "\\monteCarlo"
    try:
        os.stat(sensDir)
    except:
        os.mkdir(sensDir)
            
    #====================================    
    # Perform Simulations
    #====================================
    num_cores = multiprocessing.cpu_count() -1 # Save one core for other processes
    
    for scenarioName in scenarioNames:
    
        # Create sensitivity cases
        n_cases = 7
        cases = tt.createMonteCarloCases(scenarioInputs, scenarioName, sensitivityInputs,sensitivityMultiplier,n_cases=n_cases,path='data')
        
        # Save cases
        os.chdir(sensDir)
        cases.to_csv('MonteCarloInputs_'+scenarioName+'.csv')
        os.chdir(workDir)
                
        # Perform simulations in parallel
        with parallel_backend('multiprocessing', n_jobs=num_cores):
            outputs = Parallel(n_jobs=num_cores,verbose=5)(delayed(evaluateMonteCarlo)(modelInputs, scenarioInputs, scenarioName, paths, cases, caseNum) for caseNum in range(n_cases))     
    
        # Save results to a csv
        os.chdir(sensDir)
        df = pd.DataFrame(outputs)
        df.to_csv('MonteCarloResults_'+scenarioName+'.csv')
        os.chdir(workDir)