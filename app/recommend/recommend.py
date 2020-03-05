import json
import numpy as np
import os


path = os.path.dirname(os.path.abspath(__file__))


# 读取所有题目信息
def read_problems():
    global problems_dic
    global problems_list
    global problems_classified_in_tags
    problems_dic = {}
    problems_list = []
    problems_classified_in_tags = [[] for i in range(0, 10)]
    problem_path = path + r'/Problem_After_Cluster.txt'
    with open(problem_path, 'r') as temp_file:
        for content in temp_file:
            content = json.loads(content)
            problems_classified_in_tags[int(content['tag'])].append(content["ID"])
            problems_dic[content["ID"]] = content
            problems_list.append(content)


def read_users_ability(the_username):
    global username_ability
    global the_user_ability
    username_ability = []
    user_ability_res_path = path + r'/users_ability_res.txt'
    with open(user_ability_res_path, 'r') as temp_file:
        for content in temp_file:
            content = content.replace("'", "\"")
            # print(content)
            content = json.loads(content)
            username_ability.append(content)
            if (content['username'] == the_username):
                the_user_ability = content['ability']
                #print(the_user_ability)


def read_users_correct_problems(the_username):
    global the_user_problems_classified_in_tags
    the_user_problems_classified_in_tags = [[] for i in range(0, 10)]
    user_path = path + '/correct_problems/' + the_username + ".txt"
    with open(user_path, 'r') as temp_file:
        for content in temp_file:
            content = content.replace("'", "\"")
            content = json.loads(content)
            the_user_problems_classified_in_tags[int(content['tag'])].append(content["ID"])


def find_problems_to_be_evaluated():
    global the_user_problems_to_be_evaluated
    the_user_problems_to_be_evaluated = [{} for i in range(0, 10)]
    for problem in problems_list:
        # print(problem)
        problem_tag = int(problem['tag'])
        # print(problem['difficulty'])
        # print(the_user_ability[problem_tag])
        if problem['difficulty'] >= the_user_ability[problem_tag] and problem['difficulty'] <= the_user_ability[
            problem_tag] + 100:
            if problem['ID'] not in the_user_problems_classified_in_tags[problem_tag]:
                the_user_problems_to_be_evaluated[problem_tag][problem['ID']] = 0
    # print(the_user_problems_to_be_evaluated)


def calculate_similarity(list_1, list_2):
    float_formatter = lambda x: "%.2f" % x
    np.set_printoptions(formatter={'float_kind': float_formatter})
    length_1 = len(list_1)
    length_2 = len(list_2)
    paths = np.full((length_1 + 1, length_2 + 1), np.inf)
    paths[0, 0] = 0
    for i in range(0, length_1):
        for j in range(0, length_2):
            d = list_1[i] - list_2[j]
            paths[i + 1, j + 1] = d ** 2 + min(paths[i, j + 1], paths[i + 1, j], paths[i, j])
    return np.sqrt(paths[length_1, length_2])


def calculate_recommended_value(the_username):
    #global recommended_value_result
    recommended_value_result = [{} for i in range(0, 10)]
    i = 1
    for user_msg in username_ability:
        similarity = calculate_similarity(the_user_ability, user_msg['ability']) / 1000.0
        # print(user_msg['username'])
        if user_msg['username'] == the_username:
            continue
        #print("check No." + str(i) + " user named " + user_msg['username'] + "'s correct problems list")
        i += 1
        user_path = path + '/correct_problems/' + user_msg['username'] + ".txt"
        with open(user_path, 'r') as temp_file:
            for content in temp_file:
                content = content.replace("'", "\"")
                content = json.loads(content)
                if content['ID'] in the_user_problems_to_be_evaluated[int(content['tag'])].keys():
                    the_user_problems_to_be_evaluated[int(content['tag'])][content['ID']] += 1.0 / similarity
    for i in range(0, 10):
        recommended_value_result[i] = sorted(the_user_problems_to_be_evaluated[i].items(), key=lambda d: d[1],
                                             reverse=True)
    #print(the_user_problems_to_be_evaluated)
    #print(recommended_value_result)
    return recommended_value_result, problems_dic


# def output_result(number, the_username):
#     workbook = xlwt.Workbook(encoding='utf-8')
#     booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
#     alignment = xlwt.Alignment()  # Create Alignment
#     alignment.vert = xlwt.Alignment.VERT_CENTER
#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     style = xlwt.XFStyle()
#     style.alignment = alignment
#     row0 = ['题目编号', '推荐指数', '题目难度', '类别']
#     for i in range(0, len(row0)):
#         booksheet.write(0, i, row0[i], style)
#     i = 1
#     for problem_ID, recommended_value in recommended_value_result[number]:
#         booksheet.write(i, 0, problem_ID, style)
#         booksheet.write(i, 1, recommended_value, style)
#         booksheet.write(i, 2, problems_dic[problem_ID]['difficulty'], style)
#         booksheet.write(i, 3, number)
#         i += 1
#         if i == 50:
#             break
#     booksheet.col(1).width = 60 * 256
#     workbook.save(the_username + "RecommendResult/XLS/tag_" + str(number) + ".xls")
#     with open(the_username + "RecommendResult/TXT/tag_" + str(number) + ".txt", 'w', encoding='utf-8',
#               errors='ignore') as temp_file:
#         temp_file.write(str(recommended_value_result[number]))
#
#
# def del_file(fpath):
#     ls = os.listdir(fpath)
#     for i in ls:
#         c_path = os.path.join(fpath, i)
#         if os.path.isdir(c_path):
#             del_file(c_path)
#         else:
#             os.remove(c_path)


