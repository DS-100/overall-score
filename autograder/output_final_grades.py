#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import json


# In[ ]:


metadata = json.load(open('/autograder/submission_metadata.json', 'r'))
sid = int(metadata['users'][0]['sid'])
grades = pd.read_csv('/autograder/source/grades.csv', index_col=0).loc[sid]


# grades.loc['Rubric1'] = .4*grades['Homework Total'] + .1*grades['Lab Total'] + .1 * grades['Discussion Total'] + .16*grades['Midterm'] + .24*grades['Final']
# grades.loc['Rubric2'] = .4*grades['Homework Total'] + .1*grades['Lab Total'] + 0 * grades['Discussion Total'] + .2*grades['Midterm'] + .3*grades['Final']
# grades.loc['Overall'] = np.max(grades.loc[['Rubric1', 'Rubric2']])


# In[ ]:


gs_output = {'tests': []}


# In[ ]:


def output_homework_grades(grades, gs_output):
    hws = [f'Homework {i}' for i in range(1, 12 + 1)]
    hw_outputs = [f'Your {hw} score is {grades.loc[hw]}.' for hw in hws]
    hw_outputs = np.append(hw_outputs, [f"The following homeworks are being dropped: {grades.loc['Dropped Homeworks']}."])
    hw_outputs = np.append(hw_outputs, [f"Your overall homework score is {grades.loc['Homework Total']}."])
    gs_output['tests'].append({
        'name': 'Homeworks',
        'score': float(grades.loc['Homework Total'] * 40),
        'max_score': 40,
        'output': '\n'.join(hw_outputs)
    })


# In[ ]:


def output_lab_grades(grades, gs_output):
    labs = [f'Lab {i}' for i in range(1, 13 + 1)]
    lab_outputs = [f'Your {lab} score is {grades.loc[lab]}.' for lab in labs]
    lab_outputs = np.append(lab_outputs, [f"The following labs are being dropped: {grades.loc['Dropped Labs']}."])
    lab_outputs = np.append(lab_outputs, [f"Your overall lab score is {grades.loc['Lab Total']}."])
    gs_output['tests'].append({
        'name': 'Labs',
        'score': float(grades.loc['Lab Total'] * 10),
        'max_score': 10,
        'output': '\n'.join(lab_outputs)
    })

def output_discussion_grades(grades, gs_output):
    if grades.loc['Rubric1'] >= grades.loc['Rubric2']:
        max_score = 10
    else:
        max_score = 0

    discs = [f'Discussion {i}' for i in range(1, 13 + 1)]
    disc_outputs = [f'Your {disc} score is {grades.loc[disc]}.' for disc in discs]
    disc_outputs = np.append(disc_outputs, [f"The following discussions are being dropped: {grades.loc['Dropped Discussions']}."])
    disc_outputs = np.append(disc_outputs, [f"Your overall discussion score is {grades.loc['Discussion Total']}."])
    gs_output['tests'].append({
        'name': 'Discussions',
        'score': float(grades.loc['Discussion Total'] * max_score),
        'max_score': max_score,
        'output': '\n'.join(disc_outputs)
    })

# In[ ]:


def output_survey_grades(grades, gs_output):
    gs_output['tests'].append({
        'name': 'Weekly Surveys',
        'score': float(grades.loc['Weekly Surveys'] * 2),
        'max_score': 2,
        'output': f"You have submitted {int(8 * grades.loc['Weekly Surveys'])} weekly survey(s)."
    })


# In[ ]:


def output_project_grades(grades, gs_output):
    project_outputs = [f"Your Project 1 score is {grades.loc['Project 1']}.",                        f"Your Project 2 score is {grades.loc['Project 2']}.",                        f"Your overall project score is {np.mean([grades.loc['Project 1'], grades.loc['Project 2']])}."]
    gs_output['tests'].append({
        'name': 'Projects',
        'score': float(6 * grades.loc['Project 1']  + 6 * grades.loc['Project 2']),
        'max_score': 12,
        'output': '\n'.join(project_outputs)
    })


# In[ ]:

def output_feedback_grades(grades, gs_output):
    feedbacks = [f'Week {i} Feedback Form' for i in [3, 5, 7]]
    fb_outputs = [f'Your {fb} score is {grades.loc[fb]}.' for fb in feedbacks]
    fb_total = np.sum(grades.loc[feedbacks])
    fb_outputs = np.append(fb_outputs, [f"You submitted {fb_total} feedback forms, equaling {fb_total * .5} bonus percentage points on your midterm."])
    gs_output['tests'].append({
        'name': 'Feedback Forms',
        'score': float(grades.loc['Lab Total'] * 0),
        'max_score': 0,
        'output': '\n'.join(fb_outputs)
    })


def output_mt_grade(grades, gs_output):

    # If they are using rubric option 1 which counts discussion
    if grades.loc['Rubric1'] >= grades.loc['Rubric2']:
        max_score = 16
    else:
        max_score = 20

    # Calculate MT extra credit from feedback forms
    feedbacks = [f'Week {i} Feedback Form' for i in [3, 5, 7]]
    fb_total = np.sum(grades.loc[feedbacks]) * .005
    mt_total = grades.loc['Midterm'] + fb_total

    mt_outputs = [f"Your raw midterm exam score is {grades.loc['Midterm']}."]
    mt_outputs = np.append(mt_outputs, [f"You received {fb_total} extra credit points from filling out feedback forms."])
    mt_outputs = np.append(mt_outputs, [f"Your total midterm exam score is {mt_total}."])

    gs_output['tests'].append({
        'name': 'Midterm',
        'score': float(mt_total * max_score),
        'max_score': max_score,
        'output': "\n".join(mt_outputs)
    })

def output_overall_score(grades, gs_output):
    outputs = [f"Your score, counting discussion, would be {grades.loc['Rubric1']}"]
    outputs = np.append(outputs, f"Your score, not counting discussion, would be {grades.loc['Rubric2']}")
    outputs = np.append(outputs, f"Your overall score is {grades.loc['Overall']}")
    gs_output['tests'].append({
        'name': 'Overall Score',
        'score': 0,
        'max_score': 0,
        'output': "\n".join(outputs)
    })

# In[ ]:

def output_final_grade(grades, gs_output):
    # If they are using rubric option 1 which counts discussion
    if grades.loc['Rubric1'] >= grades.loc['Rubric2']:
        max_score = 24
    else:
        max_score = 30

    # Calculate final extra credit from official evaluation
    eval_total = grades.loc['Official Course Evaluation Proof'] * .01
    final_total = grades.loc['Final'] + eval_total

    final_outputs = [f"Your raw final exam score is {grades.loc['Final']}."]
    final_outputs = np.append(final_outputs, [f"You received {eval_total} extra credit points from filling out the official course evaluation."])
    final_outputs = np.append(final_outputs, [f"Your total final exam score is {final_total}."])

    gs_output['tests'].append({
        'name': 'Final',
        'score': float(final_total * max_score),
        'max_score': max_score,
        'output': "\n".join(final_outputs)
    })


# In[ ]:

output_overall_score(grades, gs_output)
output_homework_grades(grades, gs_output)
output_lab_grades(grades, gs_output)
output_discussion_grades(grades, gs_output)
output_feedback_grades(grades, gs_output)
#output_survey_grades(grades, gs_output)
#output_project_grades(grades, gs_output)
output_mt_grade(grades, gs_output)
output_final_grade(grades, gs_output)


# In[ ]:


out_path = '/autograder/results/results.json'
with open(out_path, 'w') as f:
    f.write(json.dumps(gs_output))
