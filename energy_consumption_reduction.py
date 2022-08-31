#!/usr/bin/env python
# coding: utf-8

# # Задача:
# 
# Нам необходимо оптимизировать производственные расходы металлургического комбината ООО «Так закаляем сталь» путём уменьшения потребление электроэнергии на этапе обработки стали. Нам предстоит построить модель, которая предскажет температуру стали(последнюю).
# 
# Для этого нам дают описание самого технологического процесса:
# 
# Сталь обрабатывают в металлическом ковше вместимостью около 100 тонн. Чтобы ковш выдерживал высокие температуры, изнутри его облицовывают огнеупорным кирпичом. Расплавленную сталь заливают в ковш и подогревают до нужной температуры графитовыми электродами. Они установлены в крышке ковша. 
# 
# Из сплава выводится сера (десульфурация), добавлением примесей корректируется химический состав и отбираются пробы. Сталь легируют — изменяют её состав — подавая куски сплава из бункера для сыпучих материалов или проволоку через специальный трайб-аппарат (англ. tribe, «масса»).
# 
# Перед тем как первый раз ввести легирующие добавки, измеряют температуру стали и производят её химический анализ. Потом температуру на несколько минут повышают, добавляют легирующие материалы и продувают сплав инертным газом. Затем его перемешивают и снова проводят измерения. Такой цикл повторяется до достижения целевого химического состава и оптимальной температуры плавки.
# 
# Тогда расплавленная сталь отправляется на доводку металла или поступает в машину непрерывной разливки. Оттуда готовый продукт выходит в виде заготовок-слябов (англ. *slab*, «плита»).

# ## Описание данных 
# Данные состоят из файлов, полученных из разных источников:
# 
# - `data_arc.csv` — данные об электродах;
# - `data_bulk.csv` — данные о подаче сыпучих материалов (объём);
# - `data_bulk_time.csv` *—* данные о подаче сыпучих материалов (время);
# - `data_gas.csv` — данные о продувке сплава газом;
# - `data_temp.csv` — результаты измерения температуры;
# - `data_wire.csv` — данные о проволочных материалах (объём);
# - `data_wire_time.csv` — данные о проволочных материалах (время).

# ## Доп.информация

# https://vulkantm.com/tehnologii/obrabotka-metalla-argonom-v-kovshe/
# 
# Развитие современного сталеплавильного производства требует совершенствования методов выплавки и технологии внепечной обработки металла для получения качественных сталей. Внепечная обработка расплава, а именно донная продувка металла инертными газами — важное звено технологического процесса производства стали на участке между сталеплавильным агрегатом и разливкой металла. В настоящее время использование донной продувки металла инертными газами позволяет:
# 
# 1.повысить производительность сталеплавильного агрегата за счет увеличения скорости химических процессов при внепечной обработки стали;
# 
# 
# 2.повысить чистоту стали по неметаллическим включениям;
# 
# 
# 3.осуществить дегазацию металла;
# 
# 4.создать оптимальные условия для процесса легирования.
# 
# 
# Таким образом, продувка металла инертными газами, через донные продувочные пробки и узлы, является эффективной технологией повышения качества разливаемой стали и решения задач ковшевой металлургии (гомогенизация, рафинирование, легирование, дегазация).

# ![povyshenie-kachestva-stali.jpg](attachment:povyshenie-kachestva-stali.jpg)

# <font color='steelblue'><b>Комментарий тимлида</b></font><br>
# <font color='green'>✔️ Описание на месте 👍🏼</font><br>

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ShuffleSplit
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import lightgbm as lgb


# In[3]:


electrode_data = pd.read_csv('./final_steel/data_arc.csv')
bulk_materials_volume = pd.read_csv('./final_steel/data_bulk.csv')
bulk_materials_time = pd.read_csv('./final_steel/data_bulk_time.csv')
alloy_blow_data = pd.read_csv('./final_steel/data_gas.csv')
temperature_data = pd.read_csv('./final_steel/data_temp.csv')
wire_material_volume = pd.read_csv('./final_steel/data_wire.csv')
wire_material_time = pd.read_csv('./final_steel/data_wire_time.csv')


# # --------------------------------------------------------

# # 1. Предварительный просмотр данных 

# ## 1.1 Данные об электродах

# In[5]:


electrode_data.info()


# In[6]:


electrode_data.head()


# ## 1.2 Данные о подаче сыпучих материалов

# In[7]:


bulk_materials_time.info()


# In[8]:


bulk_materials_time.head()


# In[9]:


bulk_materials_volume.info()


# In[10]:


bulk_materials_volume.head()


# ## 1.3 Данные о подаче газа

# In[11]:


alloy_blow_data.info()


# In[12]:


alloy_blow_data.head()


# ## 1.4 Данные о температуре

# In[13]:


temperature_data.info()


# In[14]:


temperature_data.head()


# ## Данные о подаче проволочных материалов

# In[15]:


wire_material_time.info()


# In[16]:


wire_material_time.head()


# In[17]:


wire_material_volume.info()


# In[18]:


wire_material_volume.head()


# # 2. Анализ данных 

# In[19]:


electrode_data['Конец нагрева дугой'] = pd.to_datetime(electrode_data['Конец нагрева дугой'].astype(str),                                                        format='%Y-%m-%d %H:%M:%S')


# In[20]:


temperature_data['Время замера'] = pd.to_datetime(temperature_data['Время замера'].astype(str),                                                   format='%Y-%m-%d %H:%M:%S')


# In[21]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Температура'].plot.box()
print(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Температура'].describe())


# In[22]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Температура'].plot.box()
print(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Температура'].describe())


# **Видно, что количество значений для последних и для начальных замеров отличается (2477 vs 3216), посмотрим подробнее**

# In[23]:


a = set(temperature_data.iloc[list(temperature_data.loc[temperature_data.groupby('key')['Время замера'].                                                        idxmin()]['Температура'].index)].key)


# In[24]:


len(a)


# In[25]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].                                                        idxmax()]['Температура']


# In[26]:


b = set(temperature_data.iloc[list(temperature_data.loc[temperature_data.groupby('key')['Время замера'].                                                        idxmax()]['Температура'].dropna().index)].key)


# In[27]:


len(b)


# **Получил список значений колонки key, в которых присутсвует NaN-ы, посмотрим не ошибки ли это в приборах самого измерения температуры** 

# In[28]:


set(a) - set(b)


# **Возьмём к примеру значение key=2516, и рассмотрим его подробнее**

# In[29]:


bulk_materials_volume[bulk_materials_volume['key'] == 2516]


# In[30]:


bulk_materials_time[bulk_materials_time['key'] == 2516]


# In[31]:


wire_material_time[wire_material_time['key'] == 2516]


# In[32]:


wire_material_volume[wire_material_volume['key'] == 2516]


# In[33]:


temperature_data[temperature_data['key'] == 2516]


# In[34]:


electrode_data[electrode_data['key'] == 2516]


# **Видно что количество замеров температуры(4 учитывая NaN) во не совпадает с суммарным кол-вом добавлений сыпучих и проволочных материалов (4+2), ну и просто видно что отсутсвуют значения замеров температуры (NaN), что наводит на мысль что скорее всего либо данные битые иначе как обьяснить почему даже кол-во замеров(4 с NaN), не совпадает со значениями добавлений материалов, ну либо же просто сломался прибор для измерения температуры(хотя первую температуру он всегда замеряет??). Вообщем скорее всего данные битые**  

# **Посмотрим на 'нормальные' данные в которых кол-во замеров температуры совпадает с кол-вом значений температуры**

# In[35]:


a = temperature_data.groupby(by='key').count()


# In[36]:


a[a['Время замера'] == a['Температура']]


# **И кол-во нормальных значений (2477) совпало с кол-вом нормальных последних замеров температуры, что видимо еще нас наталкивает на мысль что нужно работать лишь с этими данными, а все остальные где присутствует время замера температуры, но отсутсвует само значение температуры, отбросить!**

# In[37]:


temperature_data = temperature_data[temperature_data['key'].isin([x for x in range(1,2500)])] 


# In[38]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Температура'].plot.box()
print(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Температура'].describe())


# In[39]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Температура'].plot.box()
print(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Температура'].describe())


# **Заджоиним две таблицы и посмотрим есть ли разница между ключами данных таблиц и что в этих ключах интересного**

# In[40]:


a = electrode_data.merge(bulk_materials_time, on='key', how='right').key.unique()


# In[41]:


b = electrode_data.merge(bulk_materials_time, on='key', how='outer').key.unique()


# In[42]:


no_bulk_add = (set(b) - set(a))


# In[43]:


len(list(set(b) - set(a)))


# **Давайте получше рассмотрим данную аномалию**

# In[44]:


electrode_data[electrode_data['key'] == 51]


# In[45]:


temperature_data[temperature_data['key'] == 51]


# In[46]:


bulk_materials_time[bulk_materials_time['key'] == 51]


# In[47]:


wire_material_time[wire_material_time['key'] == 51]


# **Получается довольно странно что температуры плавления увеличиваются но при этом ни сыпучие не проволочные материалы добавляются судя по таблице, странно..... Попробуем найти те значения в которых не происходит добавления ни проволоки ни супучих материалов**

# In[48]:


a = electrode_data.merge(wire_material_time, on='key', how='right').key.unique()


# In[49]:


b = electrode_data.merge(wire_material_time, on='key', how='outer').key.unique()


# In[50]:


no_wire_add = set(b) - set(a)


# In[51]:


no_wire_add.intersection(no_bulk_add)


# **Убираем эти значения из таблицы temperature_data(Почему отсюда скорее всего спросите вы, но пару строк назад я удалил значения key из этой же таблицы, в которых кол-во замеров и кол-во измерений температуры не совпаали, поэтому получается что в этой таблице будут храниться 'хороший' значения key, которые удовлетворяют нас)**

# In[52]:


temperature_data = temperature_data[~temperature_data['key'].isin(no_wire_add.intersection(no_bulk_add))]


# # План работы 
# 
# Все результаты своей деятельности на данный момент описаны в пункте "План работы v3", поэтому постораюсь подробнее описать план своей работы:
# 
# * Вкратце опишу датасет, какие были преоставлены таблицы и для чего они
# 
# * Опишу какие методы анализа и к какие таблицы я использовал для этого анализа а также какие были найдены аномамалии в данных в результате данного анализа и как с ними я поступал, чтобы привести датасет в логически верный вариант.
# 
# * Затем опишу про features_engineering, а именно какие новые фичи я создал(Суммарный обьем добавленного сыпучего материала по ключу' 'Суммарный обьем добавленного проволочного материала по ключу','соотношение активной к реактивной мощности') и опишу зачем я это сделал
# 
# * Создал итоговую таблицу обьединенную по ключам для обучения, где кажому ключу будет соответвовать новые фичи представленные в пред.пункте а также первая температура и последняя используемая в качестве таргета.
# 
# * Опишу какие модели машинного обучения я использую, опишу какие использовал гиперпараметры модели(В результате Grid_search) и какую именно я выбрал итоговую модель после кросс-валидации, опишу что в качестве целевой метрики качества модели буду использовать MAE, по которому и будет отбираться самая лучшая модель
# 
# * Опишу какие результаты(метрика MAE) моделей были получены на тестовых выборках 

# **Новый план работы в конце**

# ## 2.1 Длительность времени между первым и последним замером температуры

# In[53]:


min_time_temp_measure = temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Время замера'].reset_index(drop=True)


# In[54]:


max_time_temp_measure = temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Время замера'].reset_index(drop=True)


# <font color='steelblue'><b>Комментарий тимлида</b></font><br>
# <font color='darkorange'>⚠️ min и max — функции Python, не нужно их переопределять, придумай другие имена переменным.</font>

# ✔️ Выполнено

# In[55]:


min_time_temp_measure.index = list(temperature_data.key.unique())
max_time_temp_measure.index = list(temperature_data.key.unique())


# In[56]:


(max_time_temp_measure - min_time_temp_measure).astype('timedelta64[s]').plot.box()
(max_time_temp_measure - min_time_temp_measure).astype('timedelta64[s]').describe()


# In[57]:


max_time_temp_measure


# In[58]:


diff_time = ((max_time_temp_measure - min_time_temp_measure).astype('timedelta64[s]'))


# In[59]:


diff_time[diff_time > 4500]


# In[60]:


electrode_data[electrode_data['key'] == 44]


# In[61]:


wire_material_time[wire_material_time['key'] == 44]


# In[62]:


bulk_materials_time[bulk_materials_time['key'] == 44]


# In[63]:


temperature_data[temperature_data['key'] == 44]


# ## 2.2 Суммарное время нагрева электродами, то есть сумму значений по всем промежуткам между запусками нагрева электродов.

# In[64]:


electrode_data = electrode_data.loc[electrode_data['key'].isin(temperature_data.key)]


# In[65]:


electrode_data['Начало нагрева дугой'] = pd.to_datetime(electrode_data['Начало нагрева дугой'].astype(str),                                                        format='%Y-%m-%d %H:%M:%S')


# In[66]:


electrode_data['diff'] = (electrode_data['Конец нагрева дугой'] - electrode_data['Начало нагрева дугой']).astype('timedelta64[s]')


# In[67]:


electrode_data.groupby('key').sum()['diff']


# In[68]:


electrode_data.groupby('key').sum()['diff'].plot.box()
electrode_data.groupby('key').sum()['diff'].describe()


# ## 2.3 Количество запусков нагрева электродами

# In[69]:


electrode_data.groupby('key').count()['Активная мощность']


# In[70]:


electrode_data.groupby('key').count()['Активная мощность'].plot.box()
electrode_data.groupby('key').count()['Активная мощность'].describe()


# ## 2.4 Среднее соотношение потребления активной и реактивной мощности.

# In[71]:


electrode_data['proportion'] = electrode_data['Активная мощность']/electrode_data['Реактивная мощность']


# In[72]:


electrode_data['proportion'].plot.box()
electrode_data['proportion'].describe()


# In[73]:


electrode_data.corr()


# In[74]:


pd.plotting.scatter_matrix(electrode_data)


# In[75]:


pd.plotting.scatter_matrix(temperature_data)


# In[76]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Температура'].plot.box()
print(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()]['Температура'].describe())


# In[77]:


temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Температура'].plot.box()
print(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()]['Температура'].describe())


# ## 2.5 Посмотрим как в среднем меняется температура в зависимости от добавления того или иного вещества 

# In[78]:


only_wire_add_key = [x for x in no_bulk_add if x not in no_bulk_add.intersection(no_wire_add)]


# In[79]:


only_bulk_add_key = [x for x in no_wire_add if x not in no_bulk_add.intersection(no_wire_add)]


# In[80]:


only_bulk_add_temp = temperature_data[temperature_data['key'].isin(only_bulk_add_key)]


# In[81]:


only_wire_add_temp = temperature_data[temperature_data['key'].isin(only_wire_add_key)]


# In[82]:


only_bulk_add_temp


# In[83]:


only_wire_add_temp


# In[84]:


diff_only_bulk = (only_bulk_add_temp.loc[only_bulk_add_temp.groupby('key')['Время замера'].idxmax()]['Температура'].reset_index(drop=True) - only_bulk_add_temp.loc[only_bulk_add_temp.groupby('key')['Время замера'].idxmin()]['Температура'].reset_index(drop=True))


# In[85]:


diff_only_wire = (only_wire_add_temp.loc[only_wire_add_temp.groupby('key')['Время замера'].idxmax()]['Температура'].reset_index(drop=True) - only_wire_add_temp.loc[only_wire_add_temp.groupby('key')['Время замера'].idxmin()]['Температура'].reset_index(drop=True))


# In[86]:


diff_only_bulk.plot.box()
diff_only_bulk.describe()


# In[87]:


diff_only_wire.plot.box()
diff_only_wire.describe()


# In[88]:


electrode_data


# **Переименуем колонку diff в diff_seconds для наглядности**

# In[89]:


electrode_data.rename(columns={'diff':'diff_seconds'}, inplace=True)


# In[90]:


electrode_data


# **Создадим фичу electricity как метрику отражающую время и энергию потраченную на нагрев смеси** 

# In[91]:


electrode_data['electricity'] = (electrode_data['Активная мощность']**2)+(electrode_data['Реактивная мощность']**2)


# In[92]:


electrode_data['electricity'] = electrode_data['electricity']**0.5


# In[93]:


electrode_data['electricity'] = electrode_data['electricity'] * electrode_data['diff_seconds']


# In[94]:


electrode_data


# In[95]:


electrode_data.groupby('key').mean()


# In[96]:


temperature_data.groupby('key').mean()


# In[97]:


electrode_data['Реактивная мощность'].plot.box()
electrode_data['Реактивная мощность'].describe()


# **Нашли аномальное значение в реактивной мощности, уберем его**

# In[98]:


electrode_data[electrode_data['Реактивная мощность'] < 0]


# In[99]:


list(electrode_data[electrode_data['key'] == 2116].index)


# In[100]:


electrode_data.describe()


# In[101]:


electrode_data.drop(list(electrode_data[electrode_data['key'] == 2116].index), inplace=True)


# In[102]:


electrode_data.describe()


# ## Обьединяем данные для получения данных для обучения  

# In[103]:


wire_material_volume.fillna(0.0, inplace=True)


# In[104]:


bulk_materials_volume.fillna(0.0, inplace=True)


# In[105]:


electrode_data.groupby('key')['electricity'].sum()


# In[106]:


electodes = electrode_data.groupby('key')['electricity'].sum().to_frame()


# In[107]:


electodes = electodes.reset_index()


# In[108]:


electodes


# In[109]:


#a = electrode_data.merge(bulk_materials_time, on='key', how='right')


# In[110]:


final_df = electodes.merge(wire_material_volume, on='key', how='left')


# In[111]:


final_df = final_df.merge(bulk_materials_volume, on='key', how='left')


# In[112]:


final_df = final_df.merge(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmin()],                          on='key', how='left')


# In[113]:


final_df = final_df.merge(temperature_data.loc[temperature_data.groupby('key')['Время замера'].idxmax()],                          on='key', how='left')


# In[114]:


final_df


# In[115]:


final_df.info()


# In[116]:


final_df.dropna(inplace=True)


# In[117]:


final_df.info()


# In[118]:


final_df = final_df.drop(['Время замера_x','Время замера_y'], axis=1)


# In[119]:


final_df


# In[120]:


final_df['Температура_y'].plot.hist()
final_df['Температура_y'].describe()


# In[121]:


final_df


# In[122]:


final_df.info()


# In[123]:


final_df = final_df.merge(alloy_blow_data, on='key', how='left')


# In[124]:


final_df.dropna(inplace=True)


# In[125]:


final_df.info()


# In[126]:


final_df.corr()


# In[127]:


final_df = final_df.drop('Wire 5', axis=1)


# # Linear_regression

# In[128]:


x = final_df.drop(['key','Температура_y'], axis=1)


# In[129]:


y = final_df['Температура_y']


# In[130]:


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12345)


# In[131]:


cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=22)


# In[132]:


lin_reg = LinearRegression()


# In[133]:


lin_reg.fit(X_train, y_train)


# In[134]:


cv_lin_reg = cross_val_score(lin_reg, X_train, y_train, cv=cv, scoring='neg_mean_absolute_error')
cv_lin_reg.mean()*(-1)


# ## DecisionTreeRegression

# In[135]:


# Hyper parameters range intialization for tuning 

parameters={"splitter":["best"],
            "max_depth" : [11,15,20,25,30,35,40],
           "min_samples_leaf":[1,2,3,4,5,6,7,8,9,10],
           "max_leaf_nodes":[None,10,20,30,40,50,60,70,80,90] }


# In[136]:


reg_decision_model=DecisionTreeRegressor(criterion='absolute_error', random_state=12345)


# In[140]:


tuning_model=GridSearchCV(reg_decision_model,param_grid=parameters,scoring='neg_mean_absolute_error',cv=cv,verbose=3)


# In[141]:


tuning_model.fit(X_train,y_train)


# In[142]:


tuning_model.best_score_


# In[143]:


tuning_model.best_params_


# ## Random Forest

# In[144]:


parametrs = { 'n_estimators': [500, 1000],
              'max_depth': range (1, 31, 10),
              'min_samples_split': [2, 4, 8]}


# In[145]:


forest = GridSearchCV(RandomForestRegressor(random_state=22), 
                      param_grid=parametrs, scoring='neg_mean_absolute_error', cv=cv)


# In[146]:


forest.fit(X_train,y_train)


# In[147]:


forest.best_params_


# In[148]:


forest.best_score_*(-1)


# ## LGBM

# In[149]:


parameters = {'max_depth': [2, 4, 6],
              'learning_rate': [0.01, 0.03, 0.1],
              'n_estimators': [100, 200, 500, 1000]}


# In[150]:


lgbm = LGBMRegressor(random_state=22)


# In[151]:


grid_cv = GridSearchCV(lgbm, parameters, scoring='neg_mean_absolute_error', cv=cv)


# In[152]:


grid_cv.fit(X_train,y_train)


# In[153]:


grid_cv.best_score_*(-1)


# In[154]:


grid_cv.best_params_


# ## Catboost

# In[155]:


parameters = {'max_depth': [2, 4, 8, 10],
              'learning_rate': [0.01, 0.03, 0.1],
              'l2_leaf_reg': [1, 3, 5],
              'iterations': [50, 100, 200]
             }


# In[156]:


catboost = CatBoostRegressor(loss_function='MAE', random_state=22)


# In[157]:


grid_search_result = catboost.grid_search(parameters, X=X_train, y=y_train, cv=cv, verbose=0, plot=True)


# In[158]:


catboost.get_params()


# In[159]:


catboost.get_best_score()


# In[160]:


d = {'model' : ["linear regression", 'Decision Tree Regressor', 'Random Forest', 'LGBM', 'Catboost'],
     'CV_MAE' : [6.652, 6.963, 6.194, 6.181, 5.543]}
df_total = pd.DataFrame(data=d)


# In[161]:


df_total


# По результатам нашей работы мы выяснили, что заказчику следует предложить модель `CatBoostRegressor` для прогнозирования температуры стали, что может привести к уменьшению затрат на электроэнергию.

# **Комментарий студента**
# 
# Хорошо все замечания посторался исправить, а теперь поскольку самая лучшая метрика у нас получилась на модели Catboost, посмотрим какие именно значения MAE у нас получатся на тестовой выборке

# In[162]:


mean_absolute_error(y_test,catboost.predict(X_test))


# Модель `CatBoostRegressor` показала точность в 6.23 градусов по метрике МАЕ на тестовой выборке. Таким образом, предсказанная температура отличается от реальной менее чем на 7 градусов.

# # Финальный отчет

# **Вопрос**: Какие пункты плана были выполнены, а какие — нет (поясните почему)?<br>
# **Ответ**: В целом смотря на свой план, я осуществил все пункты своего плана, изначально хотел сделать немного больше новых фичей(напр.суммарное кол-во добавленного проволочного/сыпчатого материала), но позже передумал, поскольку как мне показалось что скорее всего у каждого резервуара с материалов будет своя тугоплавкость что будет влиять на исход модели.<br>
# **Вопрос**:Какие ключевые шаги в решении задачи выделили?<br>
# **Ответ**: Ключевым этапом как мне кажется решения любой задачи является этап с анализом и обработкой данных поскольку от него будет зависеть на сколько модель будет правильно функционироватьпо дефолту(А конкретно это то что были найдены ключи с отсутсвующими последними температурами и ключи где отсутвовало добавление каких либо материалов). И лишь после этого этапа будут осуществляться все последующие этапы такие как создание новых фичей и подбор модели и ее гиперпараметров. 
