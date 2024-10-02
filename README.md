# Training Completion Analysis

## Overview

This Python application processes training data from a `.json` file and generates output in three formats:

1. **Training Completion Count**: Lists each training and how many people have completed it.
2. **Fiscal Year Training Completion**: Lists people who completed specific trainings during a given fiscal year (FY 2024).
3. **Expired/Expiring Trainings**: Lists people with trainings that expired or will expire within one month of a given date (Oct 1, 2023).

## How to Run

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
2. Ensure the trainings.txt file is in the same directory as the script.
3. Run the script:
   ```bash
   python script.py
4. The output will be saved as:
   - `task_1.json`: Training completion count.
   - `task_2.json`: People who completed specific trainings in FY 2024.
   - `task_3.json`: People with expired or soon-to-expire trainings.
  
