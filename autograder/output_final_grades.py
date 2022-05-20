#!/usr/bin/env python
# coding: utf-8
"""
https://gradescope-autograders.readthedocs.io/en/latest/troubleshooting/
"""

import numpy as np
import pandas as pd
import json



sid_json = json.load(open('/autograder/submission/SID.json', 'r'))
sid = int(sid_json['SID'])
# grades = pd.read_csv('/autograder/source/grades.csv', index_col=0).loc[sid]
grades = pd.read_csv('/autograder/source/grades.csv', index_col=0).loc[sid]


# grades.loc['Rubric1'] = .4*grades['Homework Total'] + .1*grades['Lab Total'] + .1 * grades['Discussion Total'] + .16*grades['Midterm'] + .24*grades['Final']
# grades.loc['Rubric2'] = .4*grades['Homework Total'] + .1*grades['Lab Total'] + 0 * grades['Discussion Total'] + .2*grades['Midterm'] + .3*grades['Final']
# grades.loc['Overall'] = np.max(grades.loc[['Rubric1', 'Rubric2']])



gs_output = {'tests': []}


#TODO: Somehow differentiate between students with/without discussion grades.

def output_homework_grades(grades, gs_output):
    if grades.loc['Course'] == "DATA C100":
        if grades.loc["Disc Option"] == 1:
            max_score = 17.5
        else:
            max_score = 22.5
    else:
        if grades.loc['Disc Option'] == 2 or grades.loc['Disc Option'] == 3:
            max_score = 15
        else:
            max_score = 20
        
        
    hws = [f'Homework {i}' for i in range(1, 8)]
    hw_outputs = [f'Your {hw} score is {grades.loc[hw]}.' for hw in hws]
    hw_outputs = np.append(hw_outputs, [f"The following homeworks are being dropped: {grades.loc['Dropped Homeworks']}."])
    hw_outputs = np.append(hw_outputs, [f"Your overall homework score is {grades.loc['Homework Total']}."])
    gs_output['tests'].append({
        'name': 'Homeworks',
        'score': float(grades.loc['Homework Total'] * max_score),
        'max_score': max_score,
        'output': '\n'.join(hw_outputs)
    })



def output_lab_grades(grades, gs_output):
    if grades.loc['Course'] == 'DATA C100':
        max_score = 10
    else:
        if grades.loc["Lab Option"] == 1:
            max_score = 5
        else:
            max_score = 0
        
    labs = [f'Lab {i}' for i in range(1, 14)]
    lab_outputs = [f'Your {lab} score is {grades.loc[lab]}.' for lab in labs]
    lab_outputs = np.append(lab_outputs, [f"The following labs are being dropped: {grades.loc['Dropped Labs']}."])
    lab_outputs = np.append(lab_outputs, [f"Your overall lab score is {grades.loc['Lab Total']}."])
    gs_output['tests'].append({
        'name': 'Labs',
        'score': float(grades.loc['Lab Total'] * max_score),
        'max_score': max_score,
        'output': '\n'.join(lab_outputs)
    })
    

def output_project_grades(grades, gs_output):
    if grades.loc['Course'] == 'DATA C100':
        max_score = 15
    else:
        if grades.loc["Lab Option"] == 1:
            max_score = 10
        else:
            max_score = 15
        
    projects = [f'Project {i}' for i in ["1A", "1B", "2A", "2B"]]
    project_outputs = [f'Your {project} score is {grades.loc[project]}.' for project in projects]
#     project_outputs = np.append(project_outputs, [f"The following projects are being dropped: {grades.loc['Dropped Labs']}."])
    project_outputs = np.append(project_outputs, [f"Your overall project score is {grades.loc['Project Total']}."])
    gs_output['tests'].append({
        'name': 'Projects',
        'score': float(grades.loc['Project Total'] * max_score),
        'max_score': max_score,
        'output': '\n'.join(project_outputs)
    })

def output_discussion_grades(grades, gs_output):
    if grades.loc['Course'] == 'DATA C100':
        if grades.loc['Disc Option'] == 1:
            max_score = 5
        else:
            max_score = 0
    else:
        if grades.loc['Disc Option'] == 2 or grades.loc['Disc Option'] == 3:
            max_score = 5
        else:
            max_score = 0
                
    
#     discs = [f'Discussion {i}' for i in range(1, 13 + 1)]
#     disc_outputs = [f'Your {disc} score is {grades.loc[disc]}.' for disc in discs]
#     disc_outputs = np.append(disc_outputs, [f"The following discussions are being dropped: {grades.loc['Dropped Discussions']}."])
    disc_outputs = [f"Your discussion score (without drops) is {grades.loc['Discussion Attendance']}."]
    disc_outputs = np.append(disc_outputs, [f"Your overall discussion score is {grades.loc['Discussion Total (Including Drops)']}."])
    gs_output['tests'].append({
        'name': 'Discussions',
        'score': float(grades.loc['Discussion Total (Including Drops)'] * max_score),
        'max_score': max_score,
        'output': '\n'.join(disc_outputs)
    })



def output_survey_grades(grades, gs_output):
    
    if grades.loc['Course'] == 'DATA C100':
        max_score = 2.5
    else:
        max_score = 0
        
    survey_outputs = [f"Your survey score (without drops) is {grades.loc['Weekly Survey']}."]
    survey_outputs = np.append(survey_outputs, [f"Your overall survey score is {grades.loc['Weekly Survey Total (Including Drops)']}."])
            
    gs_output['tests'].append({
        'name': 'Weekly Surveys',
        'score': float(grades.loc['Weekly Survey Total (Including Drops)'] * max_score),
        'max_score': max_score,
        'output': '\n'.join(survey_outputs)
    })



# def output_ugrad_project_grades(grades, gs_output):
#     if grades.loc['Sections'] == 'DATA C100':
#         max_score = 30
#     else:
#         max_score = 20
    
    
#     project_outputs = [f"Your Project Part 1 score is {grades.loc['Part 1 Score']}.",                        f"Your Project 2 score is {grades.loc['Part 2 Final Score']}.",                        f"Your overall project score is {grades.loc['Total Project Score']}."]
#     gs_output['tests'].append({
#         'name': 'Final Project',
#         'score': float(grades.loc['Total Project Score'] * max_score),
#         'max_score': max_score,
#         'output': '\n'.join(project_outputs)
#     })


# In[ ]:


def output_grad_project_grades(grades, gs_output):
    if grades.loc['Course'] == 'DATA C100':
        max_score = 0
        grad_project_score = 0
    else:
        max_score = 15
        grad_project_score = float(grades.loc['Grad Project'] * max_score)
    
    project_outputs = [f"Your Grad Project score is {grad_project_score}."]
    gs_output['tests'].append({
        'name': 'Grad Project',
        'score': grad_project_score, 
        'max_score': max_score,
        'output': '\n'.join(project_outputs)
    })

    
# In[ ]:


# def output_feedback_grades(grades, gs_output):
#     feedbacks = [f'Week {i} Feedback Form' for i in [3, 5, 7]]
#     fb_outputs = [f'Your {fb} score is {grades.loc[fb]}.' for fb in feedbacks]
#     fb_total = np.sum(grades.loc[feedbacks])
#     fb_outputs = np.append(fb_outputs, [f"You submitted {fb_total} feedback forms, equaling {fb_total * .5} bonus percentage points on your midterm."])
#     gs_output['tests'].append({
#         'name': 'Feedback Forms',
#         'score': float(grades.loc['Lab Total'] * 0),
#         'max_score': 0,
#         'output': '\n'.join(fb_outputs)
#     })


def output_mt1_grade(grades, gs_output):

    # If they are using rubric option 1 which counts discussion

    mt1_outputs = [f"Your raw midterm 1 exam score is {grades.loc['Midterm 1']}."]

    gs_output['tests'].append({
        'name': 'Midterm 1',
        'score': float(grades.loc['Midterm 1'] * grades.loc['Midterm 1 Weights'] * 100),
        'max_score': grades.loc['Midterm 1 Weights'] * 100,
        'output': "\n".join(mt1_outputs)
    })
    
def output_mt2_grade(grades, gs_output):

    # If they are using rubric option 1 which counts discussion

    mt2_outputs = [f"Your raw midterm 2 exam score is {grades.loc['Midterm 2']}."]

    gs_output['tests'].append({
        'name': 'Midterm 2',
        'score': float(grades.loc['Midterm 2'] * grades.loc['Midterm 2 Weights'] * 100),
        'max_score': grades.loc['Midterm 2 Weights'] * 100,
        'output': "\n".join(mt2_outputs)
    })

def output_final_exam_grade(grades, gs_output):

    # If they are using rubric option 1 which counts discussion

    final_exam_outputs = [f"Your raw final exam score is {grades.loc['Final Exam']}."]

    gs_output['tests'].append({
        'name': 'Final Exam',
        'score': float(grades.loc['Final Exam'] * grades.loc['Final Exam Weights'] * 100),
        'max_score': grades.loc['Final Exam Weights'] * 100,
        'output': "\n".join(final_exam_outputs)
    })

    
def output_overall_score(grades, gs_output):
    if grades.loc["Incomplete?"] == 1:
        outputs = [f"Because you requested you an incomplete, your overall score is -100"]
        score = -100
    else:
        outputs = [f"Your overall score is {grades.loc['Overall Score']}."]
        score = 0
    gs_output['tests'].append({
        'name': 'Overall Score',
        'score': score,
        'max_score': 0,
        'output': "\n".join(outputs)
    })

    # for staff use when viewing on Gradescope
    print(grades)
    print(gs_output)

# In[ ]:

# def output_final_grade(grades, gs_output):
#     # If they are using rubric option 1 which counts discussion
#     if grades.loc['Rubric1'] >= grades.loc['Rubric2']:
#         max_score = 24
#     else:
#         max_score = 30

#     # Calculate final extra credit from official evaluation
#     eval_total = grades.loc['Official Course Evaluation Proof'] * .01
#     final_total = grades.loc['Final'] + eval_total

#     final_outputs = [f"Your raw final exam score is {grades.loc['Final']}."]
#     final_outputs = np.append(final_outputs, [f"You received {eval_total} extra credit points from filling out the official course evaluation."])
#     final_outputs = np.append(final_outputs, [f"Your total final exam score is {final_total}."])

#     gs_output['tests'].append({
#         'name': 'Final',
#         'score': float(final_total * max_score),
#         'max_score': max_score,
#         'output': "\n".join(final_outputs)
#     })


output_overall_score(grades, gs_output)
output_homework_grades(grades, gs_output)
output_lab_grades(grades, gs_output)
output_project_grades(grades, gs_output)
output_discussion_grades(grades, gs_output)
#output_feedback_grades(grades, gs_output)
output_survey_grades(grades, gs_output)
output_grad_project_grades(grades, gs_output)
output_mt1_grade(grades, gs_output)
output_mt2_grade(grades, gs_output)
# output_ugrad_project_grades(grades, gs_output)
# output_grad_project_grades(grades, gs_output)
# output_final_grade(grades, gs_output)
output_final_exam_grade(grades, gs_output)


out_path = '/autograder/results/results.json'
with open(out_path, 'w') as f:
    f.write(json.dumps(gs_output))
