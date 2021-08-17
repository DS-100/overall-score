# overall-score
Scripts for generating overall score report for students, usually near the end of the semester.

### `autograder/`

Everything in this directory should be zipped into an `autograder.zip` for Gradescope configuration.

`output_final_grades.py`: Update this file according to the grading rubric. Each function should add a new test case, with the weighting and text output describing the rubric.

This directory also requires a `grades.csv` file (not included), which must contain an `SID` column, in addition to columns for each grade category and assignment.

### `api_client_2.py`

This file generates the dummy submission for each student that Gradescope then "grades" according to `output_final_grades.py` above. `COURSE_ID` and `ASSIGNMENT_ID` should be updated each semester.
