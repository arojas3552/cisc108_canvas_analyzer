"""
Project 4C
Canvas Analyzer
CISC108 Honors
Fall 2019

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Alma Rojas
"""
import matplotlib.pyplot as plt

import canvas_requests

__version__ = 7

# 1) main
'''
Consumes a string representing the user token (e.g., 'hermione')
 and calls all the other functions as shown in the diagram. 
 The main function will be graded on Web-CAT based on the functions
 you have implemented; only include the functions you have implemented,
 but make sure you correctly call all the functions you do implement
'''


def main(user_id: str):
    user = canvas_requests.get_user(user_id)
    print_user_info(user)
    course = canvas_requests.get_courses(user_id)
    courses = filter_available_courses(course)
    print_courses(courses)
    course_ids = get_course_ids(courses)
    course_id = choose_course(course_ids)
    submissions = canvas_requests.get_submissions(user_id, course_id)
    summarize_points(submissions)
    summarize_groups(submissions)
    plot_scores(submissions)
    plot_grade_trends(submissions)


##################################
# 2) print_user_info
'''
Consumes a User dictionary and prints out the user's name, title, primary email, and bio. 
It does not return anything.
 Note: this function consumes a dictionary, not a string; 
 it does NOT call the canvas_requests.get_user function, 
 it consumes the result of calling the function.
'''


def print_user_info(user: dict):
    for info in user:
        print('Name: ', user['name'])
        print('Title: ', user['title'])
        print('Primary Email: ', user['primary_email'])
        print('Bio: ', user['bio'])


##################################
# 3) filter_available_courses
'''
 Consumes a list of Course dictionaries and returns a list of Course dictionaries 
 where the workflow_state key's value is 'available' (as opposed to 'completed' or something else).
'''


def filter_available_courses(course: list) -> list:
    new_list = []
    for key in course:
        if key['workflow_state'] == 'available':
            new_list.append(course[key])
        return new_list


##################################
# 4) print_courses
'''
 Consumes a list of Course dictionaries and prints out the ID and name of each course on separate lines.
'''


def print_courses(courses: list):
    for name in courses:
        aid = str(name['id'])
        nam = str(name['name'])
        print(aid, ':', nam)


##################################
# 5) get_course_ids
'''
Consumes a list of Course dictionaries and returns a list of integers representing course IDs.
'''


def get_course_ids(courses: list) -> list:
    course_ids = []
    for items in courses:
        course_ids.append(items['id'])
        return course_ids


##################################
# 6) choose_course
'''
Consumes a list of integers representing course IDs and prompts the user to enter a valid ID,
and then returns an integer representing the user's chosen course ID. 
If the user does not enter a valid ID, the function repeatedly loops until they type in a valid ID.
You will need to use the input function to get the user's choice.
'''


def choose_course(course_ids: list):
    input_id = input("Please enter a valid ID:")
    input_id = int(input_id)
    while input_id not in course_ids:
        input_id = input("Please enter a valid ID:")
        return input_id


##################################
# 7) summarize_points
'''
Consumes a list of Submission dictionaries and prints out three summary statistics about the submissions 
where there is a score (i.e. the submissions score is not None):
-Points possible so far: The sum of the assignments' points_possible multiplied by the assignment's group_weight.
-Points obtained: The sum of the submissions' score multiplied by the assignment's group_weight.
-Current grade: the Points obtained divided by the Points possible so far, multiplied by 100 and rounded.
 Note that you can use the built-in round function.
'''


def summarize_points(sub_dicts: [dict]):
    sum_points_possible = 0
    sum_sub_score = 0
    for items in sub_dicts:
        sum_points_possible += items['assignment']['points_possible']
    for items in sub_dicts:
        if sub_dicts['score'] is not None:
            sum_sub_score += items['score']

    points_possible = sum_points_possible * sub_dicts['assignment']['group']['group_weight']
    points_obtained = sum_sub_score * sub_dicts['assignment']['group']['group_weight']
    current_grade = (points_obtained / points_possible) * 100
    round(current_grade)

    print('Points possible so far: ', points_possible)
    print('Points obtained: ', points_obtained)
    print('Current grade: ', current_grade)


##################################
# 8) summarize_groups
'''
Consumes a list of Submission dictionaries and prints out the group name and unweighted grade for each group. 
The unweighted grade is the total score for the group's submissions divided by the total 
points_possible for the group's submissions, multiplied by 100 and rounded. Like the summarize_points function, 
you should ignore the submission without a score (i.e. the submission's score is None).
You are recommended to apply the Dictionary Summing Pattern to implement this function.
This function is a little difficult, so you might want to complete the next function first.
'''


def summarize_groups(sub_dicts:[dict]):
    groups = {}
    point = {}
    for each_name in sub_dicts['assignment']['name']:
        if each_name is not None:
            name= sub_dicts['assignment']['group']['name']
            if name not in groups:
                groups[name] = 0
                point[name]= 0
            groups[name] = groups[name]+ each_name['score']
            point[name]= each_name['assignment']['points_possible'] + point[name]
    for names in groups:
        g, p = (groups[names], point[names])
        print(names, ':', round(100*g/p))



##################################
# 9) plot_scores
'''
Consumes a list of Submission dictionaries and plots each submissions' grade as a histogram. 
The grade is calculated as the submission's score multiplied by 100 and divided by the assignment's points_possible.
You should only plot the submissions that have been graded (score is not None) and the assignment is worth more than 
0 points (points_possible is not truthy). Title your graph as "Distribution of Grades", label the X-axis as "Grades",
and label the Y-axis as "Number of Assignments".
'''


def plot_scores(sub_dicts: [dict]):
    grade = []
    for items in sub_dicts:
        if items['score'] is not None and items['assignment']['points_possible'] > 0:
            grade.append(items['score'] * 100 / items['points_possible'])
    plt.hist(grade)
    plt.title("Distribution of Grades")
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.show()




##################################
# 10) plot_grade_trends
'''
Consumes a list of Submission dictionaries and plots the grade trend of the submissions as a line plot. 
The grade trend contains three lines (ordered by the assignments' due_at date) that show you the range of grades you could
get in the course:
-Highest: The running sum of graded submission scores followed by the running sum of points still possible from ungraded assignments.
-Lowest: The running sum of graded submission scores followed by the running sum if you scored 0 on all ungraded assignments.
-Maximum: The running sum of the points possible on all assignments in the course.
'''

import datetime
def plot_grade_trends(sub_dicts: [dict]):
    submissions = sub_dicts
    max_points = []
    low_points = []
    high_points = []
    dates = []
    max_score = 0
    for sub in submissions:
        dates.append(datetime.datetime.strptime(sub['assignment']['due_at'], '%Y-%m-%dT%H:%M:%SZ'))
        if sub['workflow_state'] == 'graded':
            max_points.append(100*sub['assignment']['points_possible'] * sub['assignment']['group']['group_weight'])
            low_points.append(100**sub['score']*sub['assignment']['group']['group_weight'])
            high_points.append(100**sub['score']*sub['assignment']['group']['group_weight'])
        elif sub['workflow_state'] != 'graded':
            low_points.append(0)
            high_points.append(100* sub['assignment']['points_possible'] * sub['assignment']['group']['group_weight'])
            max_points.append(100*sub['assignment']['points_possible'] * sub['assignment']['group']['group_weight'])
    max_score = sum(max_points) / 100

    running_sum_high = 0
    running_sums_high = []
    for points in high_points:
        running_sum_high = running_sum_high+points
        running_sums_high.append(running_sum_high)

    running_sum_low = 0
    running_sums_low = []
    for points in low_points:
        running_sum_low = running_sum_low +points
        running_sums_low.append(running_sum_low)

    running_sum_max = 0
    running_sums_max = []
    for points in max_points:
        running_sum_max = running_sum_max +points
        running_sums_max.append(running_sum_max)

    for items in running_sums_high:
        items = items/max_score
    for items in running_sums_low:
        items = items / max_score
    for items in running_sums_max:
        items = items / max_score
    plt.plot(dates, running_sums_high, Label='Highest')
    plt.plot(dates, running_sums_low, Label='Lowest')
    plt.plot(dates, running_sums_max, Label= 'Maximum')
    plt.legend()
    plt.title('Grade Trend')
    plt.ylabel('Grade')
    plt.show()



##################################
# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')

    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')
 TOKEN (You know, if you want)')