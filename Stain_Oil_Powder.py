#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/21 18:13
# @Author  : lanlin
# 污渍stain和油渍oil为输入变量，洗衣粉powder为输出的模糊控制基本介绍如下链接
# https://blog.csdn.net/dcyywin8/article/details/103460871


import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

''' 步骤1.设置各个变量范围[1,2,...,10] '''
x_stain_range = np.arange(1, 11, 1, np.float32)
x_oil_range = np.arange(1, 11, 1, np.float32)
y_powder_range = np.arange(1, 11, 1, np.float32)


''' 步骤2.定义输入输出模糊集和其隶属度函数（使用三角函数），同时定义输出解模糊规则 '''
# 创建模糊控制变量
x_stain = ctrl.Antecedent(x_stain_range, 'stain')
x_oil = ctrl.Antecedent(x_oil_range, 'oil')
y_powder = ctrl.Consequent(y_powder_range, 'powder')

# 定义模糊集和其隶属度函数
x_stain['N'] = fuzz.trimf(x_stain_range, [1, 1, 5])
x_stain['M'] = fuzz.trimf(x_stain_range, [1, 5, 10])
x_stain['P'] = fuzz.trimf(x_stain_range, [5, 10, 10])

x_oil['N'] = fuzz.trimf(x_oil_range, [1, 1, 5])
x_oil['M'] = fuzz.trimf(x_oil_range, [1, 5, 10])
x_oil['P'] = fuzz.trimf(x_oil_range, [5, 10, 10])

y_powder['N'] = fuzz.trimf(y_powder_range, [1, 1, 5])
y_powder['M'] = fuzz.trimf(y_powder_range, [1, 5, 10])
y_powder['P'] = fuzz.trimf(y_powder_range, [5, 10, 10])

# 设定输出powder的解模糊方法——质心解模糊方式
y_powder.defuzzify_method = 'centroid'


''' 步骤3.建立模糊控制规则，并初始化控制系统和运行环境 '''
# 输出为N的规则
rule0 = ctrl.Rule(antecedent=((x_stain['N'] & x_oil['N']) |
                              (x_stain['M'] & x_oil['N']) ),
                  consequent=y_powder['N'], label='rule N')

# 输出为M的规则
rule1 = ctrl.Rule(antecedent=((x_stain['P'] & x_oil['N']) |
                              (x_stain['N'] & x_oil['M']) |
                              (x_stain['M'] & x_oil['M']) |
                              (x_stain['P'] & x_oil['M']) |
                              (x_stain['N'] & x_oil['P']) ),
                  consequent=y_powder['M'], label='rule M')

# 输出为P的规则
rule2 = ctrl.Rule(antecedent=((x_stain['M'] & x_oil['P']) |
                              (x_stain['P'] & x_oil['P']) ),
                  consequent=y_powder['P'], label='rule P')

# 模糊库系统和运行环境初始化
system = ctrl.ControlSystem(rules=[rule0, rule1, rule2])
sim = ctrl.ControlSystemSimulation(system)


''' 步骤4.系统建立完成后，通过输入变量值来查看系统的输出 '''
sim.input['stain'] = 4
sim.input['oil'] = 7
sim.compute()  # 运行系统
output_powder = sim.output['powder']  # 解模糊
print(output_powder)  # 打印输出结果

