# overall-score
Scripts for generating overall score report for students, usually near the end of the semester.

### `autograder/`

Everything in this directory will be zipped into an `autograder.zip` for Gradescope configuration. 

`output_final_grades.py`: Update this file according to the grading rubric. Each function should add a new test case, with the weighting and text output describing the rubric.

* Cautionary tale: If any of the test cases have a NaN score, the Gradescope autograder will timeout mysteriously, and SSH debugging will not help (after all, you will still generate a valid `results.json`). We learned this the hard way in Spring 2022.

This directory also requires a `grades.csv` file (not included), which must contain an `SID` column, in addition to columns for each grade category and assignment.

### `api_client_2.py`

This file generates the dummy submission for each student that Gradescope then "grades" according to `output_final_grades.py` above.

* `COURSE_ID` and `ASSIGNMENT_ID` should be updated each semester.
* The script generates an `SID.json` for each student which is uploaded as the student dummy submission. This is the SID used in `output_final_grades.py`.

### Releasing Score Reports

1. Upload the autograder zip. Note that the zip should contain only the files and not the top-level `autograder` directory, as below:

    ```
    zip autograder.zip autograder/*
    ```

1. Generate the dummy submissions on your local machine by running:

    ```
    python3 api_client_2.py
    ```

    If the autograder exists for this submission, running this script will trigger the autograder to run on each new submission.

1. To debug the autograder:

    1. Re-upload just the autograder, i.e., perform Step 1 above. Don't do Step 2.

    1. On the "Configure Autograder" page, wait for the Docker image to build, then click "Test Autograder" and upload a student submission to your own account. 

    1. Use SSH, etc., to debug.

    1. When you verify it works on your own submission, then go to "Manage Submissions" -> "Regrade All Submissions."
