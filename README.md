# temoatools installation

install as a python package for anaconda distribution

1) git clone to target folder
2) From within anaconda2 prompt
    1) Change directory to the temoatools folder
        >cd C:\\temoatools
    2) Install using pip command
        >pip install .

temoatools should now be available as a package

to test:
> import temoatools as tt

# Stochastic optimization
Instructions to run examples/puerto_rico_stoch.

1) Install python and required packages
    1) Install python 2.7 (using anaconda2), https://www.anaconda.com/distribution/#download-section
    2) Install pyomo version 4.3 (using anaconda2 prompt)
        >pip install pyomo==4.3
    3) Update pyomo using legacy files
        1) Go to the temoa_stochastic/tools/legacy_files folder to find ef_writer_script_old.py. 
        Copy paste this script at: ../anaconda/lib/python2.7/site-packages/pyomo/pysp
        2) Go to the temoa_stochastic/tools/legacy_files folder to find scenariomodels.py.
        Copy paste this script at: ../anaconda/lib/python2.7/site-packages/pyomo/pysp/util 
    4) Install temoatools (instructions above). This will include copying a version of temoa (temoa_stochastic) that has been modified for this analysis
    5) Install a linear solver such as CPLEX, additional information can be found here: https://temoacloud.com/download/

2) Enter/update simulation data in examples/puerto_rico_stoch/data folder. Scenarios_overview.ppt/.pdf provides background on cases simulated
    1) paths.xls - provides paths to anaconda2 and temoa installation
    2) data_*.xls - model data
    2) scenarios.xls - variations detailed for each case/scenarios
    3) sensitivityVariables.xls - used to indicate which temoa variables are considered in a sensitivity study

3) Create input files for temoa
    1) Run examples/puerto_rico_stoch/stochastics_write_input_files.py to create files for temoa
    2) Move input files from examples/puerto_rico_stoch/stoch_inputs/ to temoa installation
        1) config_stoch_*.txt files to temoa_stochastic/temoa_model/
        2) stoch_*.py files to temoa_stochastic/tools/options/
        3) *.dat and *.sqlite files to temoa_stochastic/data_files/

4) To run a single input file (example shown for the case T_0)
    1) Single run
        1) Run the following command to generate the scenario tree - This command will create a directory that includes the information related to the stochastic scenario tree
            >python generate_scenario_tree_JB.py options/stoch_T_0.py --debug
        2) Update the scenario tree
            > python rewrite_tree_nodes.py options/stoch_T_0.py --debug
        3) Run the model in temoa
            > python temoa_model/temoa_stochastic.py --config=temoa_model/config_stoch_T_0.txt
    2) Multiple runs - To run multiple scenarios, paramaterize in batch files, examples shown in temoa_stochastic/PR_stochastic_createScenarios_all.bat and temoa_stochastic/PR_stochastic_run_all.bat

5) Analyze results (scripts in examples/puerto_rico_stoch/)
    1) Analyze optimized results
        > python stochastics_analyze_nocases.py
    2) Analyze case-based results
        > python stochastics_analyze_cases.py

6) Plot results (performed in R, scripts in examples/puerto_rico_stoch/results/)
                                                                                                                                                                                                                                                                                                                   